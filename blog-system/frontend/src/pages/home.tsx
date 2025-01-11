import { useEffect, useState } from "react";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { fetchPosts, type BlogPost } from "@/lib/api";
import { Helmet } from "react-helmet";
import { format } from "date-fns";
import { Link } from "react-router-dom";

export function HomePage() {
  const [posts, setPosts] = useState<BlogPost[]>([]);

  useEffect(() => {
    fetchPosts().then(data => setPosts(data.items));
  }, []);

  return (
    <>
      <Helmet>
        <title>Blog - Latest Posts</title>
        <meta name="description" content="Read our latest blog posts about various topics" />
        <meta name="keywords" content="blog, posts, articles" />
        <link rel="canonical" href="/" />
      </Helmet>
      
      <div className="space-y-8">
        <h1 className="text-4xl font-bold">Latest Posts</h1>
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
      </div>
    </>
  );
}
