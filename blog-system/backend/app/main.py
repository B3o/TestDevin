from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi_pagination import Page, add_pagination, paginate
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
import feedgen.feed
from slugify import slugify

from . import models
from . import schemas
from .database import engine, get_db

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="Blog System API",
    description="A blog system with SEO optimization",
    version="1.0.0"
)

# Disable CORS. Do not remove this for full-stack development.
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allows all origins
    allow_credentials=True,
    allow_methods=["*"],  # Allows all methods
    allow_headers=["*"],  # Allows all headers
)

@app.get("/healthz")
async def healthz():
    return {"status": "ok"}

@app.post("/posts/", response_model=schemas.BlogPost)
async def create_post(post: schemas.BlogPostCreate, db: Session = Depends(get_db)):
    db_post = models.BlogPost(
        **post.model_dump(),
        slug=slugify(post.title)
    )
    db.add(db_post)
    db.commit()
    db.refresh(db_post)
    return db_post

@app.get("/posts/", response_model=Page[schemas.BlogPost])
async def list_posts(db: Session = Depends(get_db)):
    posts = db.query(models.BlogPost).filter(models.BlogPost.is_published == True).order_by(models.BlogPost.created_at.desc()).all()
    return paginate(posts)

@app.get("/posts/{slug}", response_model=schemas.BlogPost)
async def get_post(slug: str, db: Session = Depends(get_db)):
    post = db.query(models.BlogPost).filter(models.BlogPost.slug == slug).first()
    if post is None:
        raise HTTPException(status_code=404, detail="Post not found")
    return post

@app.get("/sitemap.xml")
async def sitemap(db: Session = Depends(get_db)):
    """Generate sitemap for SEO"""
    posts = db.query(models.BlogPost).filter(models.BlogPost.is_published == True).all()
    
    xml_content = ['<?xml version="1.0" encoding="UTF-8"?>']
    xml_content.append('<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">')
    
    # Add homepage
    xml_content.append('  <url>')
    xml_content.append('    <loc>https://yourblog.com/</loc>')
    xml_content.append('    <changefreq>daily</changefreq>')
    xml_content.append('    <priority>1.0</priority>')
    xml_content.append('  </url>')
    
    # Add blog posts
    for post in posts:
        xml_content.append('  <url>')
        xml_content.append(f'    <loc>https://yourblog.com/posts/{post.slug}</loc>')
        xml_content.append(f'    <lastmod>{post.updated_at or post.created_at}</lastmod>')
        xml_content.append('    <changefreq>weekly</changefreq>')
        xml_content.append('    <priority>0.8</priority>')
        xml_content.append('  </url>')
    
    xml_content.append('</urlset>')
    
    return Response(content='\n'.join(xml_content), media_type="application/xml")

@app.get("/feed/rss")
async def rss_feed(db: Session = Depends(get_db)):
    """Generate RSS feed for blog posts"""
    fg = feedgen.feed.FeedGenerator()
    fg.id('https://yourblog.com/')
    fg.title('Your Blog')
    fg.description('Latest blog posts')
    fg.link(href='https://yourblog.com')
    fg.language('en')
    
    posts = db.query(models.BlogPost).filter(models.BlogPost.is_published == True).order_by(models.BlogPost.created_at.desc()).limit(10).all()
    
    for post in posts:
        fe = fg.add_entry()
        fe.id(f'https://yourblog.com/posts/{post.slug}')
        fe.title(post.title)
        fe.description(post.meta_description or '')
        fe.link(href=f'https://yourblog.com/posts/{post.slug}')
        fe.published(post.created_at)
        if post.updated_at:
            fe.updated(post.updated_at)
    
    return Response(content=fg.rss_str(pretty=True), media_type="application/rss+xml", headers={"Content-Type": "application/rss+xml; charset=utf-8"})

# Add pagination support
add_pagination(app)
