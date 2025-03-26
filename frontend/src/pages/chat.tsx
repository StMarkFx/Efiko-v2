import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '@/hooks/useAuth';
import ChatInterface from '@/components/chat/ChatInterface';
import MainLayout from '@/components/layout/MainLayout';

export default function Chat() {
  const { user, loading } = useAuth();
  const router = useRouter();

  useEffect(() => {
    if (!loading && !user) {
      router.push('/login');
    }
  }, [user, loading, router]);

  if (loading) {
    return (
      <MainLayout>
        <div className="flex items-center justify-center min-h-[60vh]">
          <div className="animate-spin rounded-full h-8 w-8 border-b-2 border-primary"></div>
        </div>
      </MainLayout>
    );
  }

  if (!user) {
    return null;
  }

  return (
    <MainLayout>
      <div className="max-w-4xl mx-auto">
        <div className="mb-8">
          <h1 className="text-3xl font-bold">Chat with AI</h1>
          <p className="text-muted-foreground mt-2">
            Ask questions about your uploaded documents and get instant answers.
          </p>
        </div>
        <ChatInterface />
      </div>
    </MainLayout>
  );
} 