import { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import { fetchPost, type BlogPost } from "@/lib/api";
import { format } from "date-fns";
import { Helmet } from "react-helmet";
import { Skeleton } from "@/components/ui/skeleton";

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

      <article className="max-w-3xl mx-auto prose prose-slate">
        <h1>{post.title}</h1>
        <div className="text-muted-foreground">
          {format(new Date(post.created_at), 'PPP')}
          {post.updated_at && ` (Updated: ${format(new Date(post.updated_at), 'PPP')})`}
        </div>
        <div className="mt-8" dangerouslySetInnerHTML={{ __html: post.content }} />
      </article>
    </>
  );
}
