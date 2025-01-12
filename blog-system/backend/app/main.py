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

# Add sample blog posts
def create_sample_posts():
    db = next(get_db())
    sample_posts = [
        {
            "title": "使用Three.js构建赛博朋克城市天际线",
            "content": """# 使用Three.js构建赛博朋克城市天际线

在这个由Three.js构建的赛博朋克小世界里，我们将探索如何创建一个充满未来感的城市天际线。本文将详细介绍实现过程和关键技术点。

## 核心技术要素

### 1. 基础场景搭建
- 场景（Scene）和相机设置
- 像素化渲染效果实现
- 雾气效果（FogExp2）配置
- 环境光照和点光源布置

### 2. 建筑生成系统
```javascript
// 创建建筑物
const cityGeometry = new THREE.BoxGeometry(1, 1, 1);
const buildingMaterial = new THREE.MeshPhongMaterial({
    color: 0x0a0a0a,
    emissive: 0x000000,
    specular: 0x111111,
    shininess: 30,
    flatShading: true
});

// 随机生成建筑物
for (let i = 0; i < 100; i++) {
    const building = new THREE.Mesh(cityGeometry, buildingMaterial);
    const height = Math.random() * 4 + 1;
    building.scale.set(0.5, height, 0.5);
    building.position.set(
        Math.random() * 20 - 10,
        height / 2,
        Math.random() * 20 - 10
    );
    scene.add(building);
}
```

### 3. 霓虹效果实现
- Bloom后期处理
- 自发光材质配置
- 动态光强变化

### 4. 优化技巧
- 实例化渲染（Instancing）
- 合理的LOD设置
- 后期处理性能优化
- 着色器优化策略

## 进阶特效

### 1. 体积光实现
```glsl
// 体积光片段着色器
void mainImage(out vec4 fragColor, in vec2 fragCoord) {
    vec2 uv = fragCoord/iResolution.xy;
    vec3 col = 0.5 + 0.5*cos(iTime+uv.xyx+vec3(0,2,4));
    fragColor = vec4(col,1.0);
}
```

### 2. 反射效果
- 环境贴图使用
- 实时反射计算
- PBR材质设置

## 性能优化建议
1. 使用合适的几何体层级
2. 优化光照计算
3. 合理使用后期处理
4. 实现细节层次控制

记住，创建一个引人入胜的赛博朋克场景不仅需要技术实现，还需要艺术设计的配合。合理的配色、光影和氛围营造都是关键要素。
""",
            "meta_description": "深入探讨使用Three.js创建赛博朋克风格的城市天际线，包括建筑生成、霓虹效果、体积光等技术实现细节。",
            "keywords": "Three.js, WebGL, 赛博朋克, 城市天际线, 3D图形, 霓虹效果, 体积光, 技术实现",
            "slug": "building-cyberpunk-skyline-with-threejs"
        },
        {
            "title": "WebGL中实现赛博朋克体积光效果",
            "content": """# WebGL中实现赛博朋克体积光效果

体积光是赛博朋克场景中不可或缺的视觉元素，本文将详细介绍如何在WebGL中实现这一效果。

## 基础原理
体积光的实现主要基于光线步进（Ray Marching）技术，通过在视线方向上采样来模拟光线在介质中的散射效果。

### 核心实现
```glsl
// 体积光着色器
uniform vec3 lightPosition;
uniform vec3 lightColor;
varying vec2 vUv;

float volumetricLight(vec3 start, vec3 end, vec3 rayDir) {
    float intensity = 0.0;
    float decay = 0.95;
    float exposure = 0.5;
    
    for(int i = 0; i < 100; i++) {
        vec3 pos = start + rayDir * float(i) * 0.01;
        float dist = distance(pos, lightPosition);
        intensity += exp(-dist) * decay;
        decay *= 0.97;
    }
    
    return intensity * exposure;
}

void main() {
    vec3 rayDir = normalize(cameraPosition - worldPosition);
    float light = volumetricLight(worldPosition, lightPosition, rayDir);
    gl_FragColor = vec4(lightColor * light, 1.0);
}
```

## 优化技巧
1. 采样次数与质量平衡
2. 使用噪声打破均匀性
3. 深度信息结合
4. 性能优化策略

## 高级效果
- 多光源处理
- 颜色渐变
- 动态变化
- 与场景交互

本文的完整实现请参考代码仓库。
""",
            "meta_description": "探索在WebGL中实现赛博朋克风格体积光效果的技术细节，包括着色器编写、优化技巧和高级效果实现。",
            "keywords": "WebGL, 体积光, 着色器, GLSL, 赛博朋克, 图形编程, 光线步进",
            "slug": "volumetric-lighting-in-webgl"
        },
        {
            "title": "赛博朋克场景性能优化指南",
            "content": """# 赛博朋克场景性能优化指南

在构建复杂的赛博朋克3D场景时，性能优化是一个关键挑战。本文将分享一些实用的优化技巧。

## 几何体优化

### 1. 实例化渲染
```javascript
// 使用InstancedMesh优化重复物体
const geometry = new THREE.BoxGeometry();
const material = new THREE.MeshPhongMaterial();
const instances = 1000;

const mesh = new THREE.InstancedMesh(geometry, material, instances);
const matrix = new THREE.Matrix4();

for (let i = 0; i < instances; i++) {
    matrix.setPosition(
        Math.random() * 100 - 50,
        Math.random() * 100,
        Math.random() * 100 - 50
    );
    mesh.setMatrixAt(i, matrix);
}
```

### 2. LOD（细节层次）
- 距离检测
- 模型简化
- 动态加载

## 着色器优化

### 1. 计算优化
```glsl
// 优化前
float intensity = pow(max(dot(normal, lightDir), 0.0), 32.0);

// 优化后
float NdotL = max(dot(normal, lightDir), 0.0);
float intensity = NdotL * NdotL * NdotL * NdotL * NdotL; // 5次相乘代替pow
```

### 2. 纹理优化
- 合理的纹理大小
- 压缩格式
- 纹理图集

## 渲染优化
1. 视锥体剔除
2. 遮挡剔除
3. 批处理优化
4. 后期处理效率

## 内存管理
- 资源释放
- 缓存控制
- 异步加载

记住，性能优化是一个持续的过程，需要根据具体场景和目标平台来调整策略。
""",
            "meta_description": "学习赛博朋克3D场景的性能优化技巧，包括几何体优化、着色器优化、渲染优化和内存管理等关键主题。",
            "keywords": "性能优化, Three.js, WebGL, 3D场景, 赛博朋克, 实例化渲染, LOD, 着色器优化",
            "slug": "cyberpunk-scene-performance-optimization"
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

# Add pagination support
add_pagination(app)
