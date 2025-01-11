const API_URL = import.meta.env.VITE_API_URL;

export interface BlogPost {
  id: number;
  title: string;
  content: string;
  slug: string;
  meta_description: string | null;
  keywords: string | null;
  created_at: string;
  updated_at: string | null;
}

export async function fetchPosts(): Promise<{ items: BlogPost[] }> {
  const response = await fetch(`${API_URL}/posts`);
  if (!response.ok) throw new Error('Failed to fetch posts');
  return response.json();
}

export async function fetchPost(slug: string): Promise<BlogPost> {
  const response = await fetch(`${API_URL}/posts/${slug}`);
  if (!response.ok) throw new Error('Failed to fetch post');
  return response.json();
}

export async function createPost(data: { 
  title: string;
  content: string;
  meta_description?: string;
  keywords?: string;
}): Promise<BlogPost> {
  const response = await fetch(`${API_URL}/posts`, {
    method: 'POST',
    headers: {
      'Content-Type': 'application/json',
    },
    body: JSON.stringify(data),
  });
  if (!response.ok) throw new Error('Failed to create post');
  return response.json();
}
