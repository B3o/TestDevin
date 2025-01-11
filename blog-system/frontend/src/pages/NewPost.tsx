import { useState } from 'react';
import ReactQuill from 'react-quill';
import 'react-quill/dist/quill.snow.css';
import { Button } from '../components/ui/button';
import { Input } from '../components/ui/input';
import { Card, CardContent, CardHeader, CardTitle } from '../components/ui/card';
import { Helmet } from 'react-helmet';
import { useNavigate } from 'react-router-dom';
import { PenLine } from 'lucide-react';
import { createPost } from '../lib/api';

export function NewPost() {
  const [title, setTitle] = useState('');
  const [content, setContent] = useState('');
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();

  const handleCreate = async () => {
    try {
      setLoading(true);
      const post = await createPost({
        title,
        content,
        meta_description: content.substring(0, 160).replace(/<[^>]*>/g, ''),
        keywords: title.split(' ').join(','),
      });
      navigate(`/posts/${post.slug}`);
    } catch (error) {
      console.error('Failed to create post:', error);
    } finally {
      setLoading(false);
    }
  };

  return (
    <>
      <Helmet>
        <title>创建新文章 - 博客系统</title>
        <meta name="description" content="使用富文本编辑器创建新的博客文章" />
      </Helmet>

      <Card className="max-w-4xl mx-auto">
        <CardHeader>
          <CardTitle className="flex items-center gap-2">
            <PenLine className="h-6 w-6" />
            创建新文章
          </CardTitle>
        </CardHeader>
        <CardContent className="space-y-4">
          <div className="space-y-2">
            <Input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="输入文章标题"
              className="text-lg"
            />
          </div>
          <div className="min-h-[400px]">
            <ReactQuill
              value={content}
              onChange={setContent}
              theme="snow"
              placeholder="开始写作..."
              modules={{
                toolbar: [
                  [{ header: [1, 2, 3, false] }],
                  ['bold', 'italic', 'underline', 'strike'],
                  [{ list: 'ordered' }, { list: 'bullet' }],
                  ['link', 'image'],
                  ['clean'],
                ],
              }}
            />
          </div>
          <div className="flex justify-end gap-2">
            <Button variant="outline" onClick={() => navigate('/')}>
              取消
            </Button>
            <Button onClick={handleCreate} disabled={loading}>
              {loading ? '发布中...' : '发布文章'}
            </Button>
          </div>
        </CardContent>
      </Card>
    </>
  );
}
