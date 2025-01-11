from fastapi import FastAPI, Depends, HTTPException, Response
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from .routes import upload
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

# Add sample blog posts
def create_sample_posts():
    db = next(get_db())
    sample_posts = [
        {
            "title": "Getting Started with FastAPI",
            "content": """# Getting Started with FastAPI

FastAPI is a modern, fast (high-performance) web framework for building APIs with Python 3.6+ based on standard Python type hints.

## Key Features
- Fast: Very high performance, on par with NodeJS and Go
- Fast to code: Increase the speed to develop features by about 200% to 300%
- Fewer bugs: Reduce about 40% of human (developer) induced errors
- Intuitive: Great editor support. Completion everywhere. Less time debugging
- Easy: Designed to be easy to use and learn. Less time reading docs
- Short: Minimize code duplication. Multiple features from each parameter declaration

## Why FastAPI?
FastAPI stands on the shoulders of giants:
- Starlette for the web parts
- Pydantic for the data parts
""",
            "meta_description": "Learn about FastAPI, a modern Python web framework for building high-performance APIs with type hints and automatic documentation generation.",
            "keywords": "FastAPI, Python, API, web framework, performance, type hints",
            "slug": "getting-started-with-fastapi"
        },
        {
            "title": "Understanding SEO Best Practices",
            "content": """# SEO Best Practices for Modern Websites

Search Engine Optimization (SEO) is crucial for improving your website's visibility in search results.

## Key SEO Elements
1. Quality Content
2. Meta Tags
3. Site Structure
4. Mobile Optimization
5. Page Speed

## Implementation Tips
- Use descriptive URLs
- Optimize images
- Create quality backlinks
- Implement proper header structure
- Regular content updates
""",
            "meta_description": "Discover essential SEO best practices for modern websites, including meta tags, content optimization, and technical considerations.",
            "keywords": "SEO, meta tags, content optimization, website optimization, search engine",
            "slug": "understanding-seo-best-practices"
        },
        {
            "title": "Building Modern Web Applications",
            "content": """# Modern Web Application Architecture

Learn about the best practices for building scalable web applications.

## Key Components
1. Frontend Framework (React/Vue/Angular)
2. Backend API
3. Database
4. Caching Layer
5. Authentication

## Best Practices
- Use TypeScript for type safety
- Implement proper error handling
- Follow REST/GraphQL principles
- Optimize for performance
- Regular security audits
""",
            "meta_description": "Explore modern web application architecture and best practices for building scalable, maintainable applications.",
            "keywords": "web development, architecture, scalability, best practices, modern web",
            "slug": "building-modern-web-applications"
        }
    ]
    
    for post_data in sample_posts:
        post = models.BlogPost(
            title=post_data["title"],
            content=post_data["content"],
            meta_description=post_data["meta_description"],
            keywords=post_data["keywords"],
            slug=post_data["slug"]
        )
        db.add(post)
    
    db.commit()

create_sample_posts()

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

@app.get("/")
async def read_root():
    return {"message": "Welcome to the Blog System API"}

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

@app.get("/posts", response_model=Page[schemas.BlogPost])
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

# Mount static files directory
app.mount("/static", StaticFiles(directory="static"), name="static")

# Include routers
app.include_router(upload.router, prefix="/api")

# Add pagination support
add_pagination(app)
