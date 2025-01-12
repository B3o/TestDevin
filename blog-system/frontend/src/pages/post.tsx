import { useEffect, useState } from "react";
import { useParams, Link } from "react-router-dom";
import { fetchPost, type BlogPost } from "@/lib/api";
import { format } from "date-fns";
import { Helmet } from "react-helmet";
import { Skeleton } from "@/components/ui/skeleton";
import { Button } from "@/components/ui/button";
import { ArrowLeft, Calendar } from "lucide-react";

export function PostPage() {
  const { slug } = useParams<{ slug: string }>();
  const [post, setPost] = useState<BlogPost | null>(null);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (slug) {
      setLoading(true);
      fetchPost(slug)
        .then(setPost)
        .finally(() => setLoading(false));
    }
  }, [slug]);

  if (loading) {
    return (
      <div className="max-w-3xl mx-auto space-y-4">
        <Skeleton className="h-12 w-3/4" />
        <Skeleton className="h-6 w-1/4" />
        <Skeleton className="h-48" />
      </div>
    );
  }

  if (!post) return null;

  return (
    <>
      <Helmet>
        <title>{post.title}</title>
        <meta name="description" content={post.meta_description || ''} />
        <meta name="keywords" content={post.keywords || ''} />
        <link rel="canonical" href={`/posts/${post.slug}`} />
        <meta property="og:title" content={post.title} />
        <meta property="og:description" content={post.meta_description || ''} />
        <meta property="og:type" content="article" />
        <meta property="article:published_time" content={post.created_at} />
        {post.updated_at && (
          <meta property="article:modified_time" content={post.updated_at} />
        )}
      </Helmet>

      <div className="max-w-3xl mx-auto">
        <Button variant="ghost" asChild className="mb-8">
          <Link to="/" className="flex items-center space-x-2">
            <ArrowLeft className="h-4 w-4" />
            <span>返回文章列表</span>
          </Link>
        </Button>

        <article className="prose prose-invert prose-headings:text-neon-cyan prose-a:text-neon-pink hover:prose-a:text-neon-pink/80 max-w-none">
          <h1 className="mb-4 hover-glow">{post.title}</h1>
          <div className="flex items-center space-x-2 text-neon-green/70 mb-8">
            <Calendar className="h-4 w-4" />
            <span>
              {format(new Date(post.created_at), 'PPP')}
              {post.updated_at && ` (更新于: ${format(new Date(post.updated_at), 'PPP')})`}
            </span>
          </div>
          <div 
            className="mt-8 prose-code:bg-card prose-code:text-neon-cyan prose-pre:bg-card prose-pre:border prose-pre:border-neon-cyan/20" 
            dangerouslySetInnerHTML={{ __html: post.content }} 
          />
        </article>
      </div>
    </>
  );
}
