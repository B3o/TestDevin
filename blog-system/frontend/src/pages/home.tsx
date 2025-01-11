import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { fetchPosts, type BlogPost } from "@/lib/api";
import { Helmet } from "react-helmet";
import { format } from "date-fns";
import { Link } from "react-router-dom";
import { Newspaper } from "lucide-react";
import { PixelWorld } from "@/components/PixelWorld";

export function HomePage() {
  const [posts, setPosts] = useState<BlogPost[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    fetchPosts()
      .then(data => setPosts(data.items))
      .finally(() => setLoading(false));
  }, []);

  return (
    <>
      <Helmet>
        <title>技术博客 - 最新文章</title>
        <meta name="description" content="阅读关于FastAPI、SEO优化、Web开发等主题的最新技术文章" />
        <meta name="keywords" content="技术博客, FastAPI, SEO, Web开发, 编程" />
        <link rel="canonical" href="/" />
      </Helmet>
      
      <div className="space-y-8">
        <PixelWorld />
        <div className="flex items-center space-x-4 mt-8">
          <Newspaper className="h-8 w-8" />
          <h1 className="text-4xl font-bold">最新文章</h1>
        </div>
        
        {loading ? (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {[1, 2, 3].map(i => (
              <Card key={i} className="h-64">
                <CardHeader>
                  <div className="h-6 bg-gray-200 rounded w-3/4"></div>
                  <div className="h-4 bg-gray-200 rounded w-1/4"></div>
                </CardHeader>
                <CardContent>
                  <div className="space-y-2">
                    <div className="h-4 bg-gray-200 rounded"></div>
                    <div className="h-4 bg-gray-200 rounded w-5/6"></div>
                  </div>
                </CardContent>
              </Card>
            ))}
          </div>
        ) : (
          <div className="grid gap-6 md:grid-cols-2 lg:grid-cols-3">
            {posts.map(post => (
              <Link key={post.id} to={`/posts/${post.slug}`}>
                <Card className="h-full hover:shadow-lg transition-shadow">
                  <CardHeader>
                    <CardTitle className="line-clamp-2">{post.title}</CardTitle>
                    <CardDescription>{format(new Date(post.created_at), 'PPP')}</CardDescription>
                  </CardHeader>
                  <CardContent>
                    <p className="text-muted-foreground line-clamp-3">
                      {post.meta_description || post.content}
                    </p>
                  </CardContent>
                </Card>
              </Link>
            ))}
          </div>
        )}
      </div>
    </>
  );
}
