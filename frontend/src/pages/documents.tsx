import { useEffect } from 'react';
import { useRouter } from 'next/router';
import { useAuth } from '@/hooks/useAuth';
import DocumentUpload from '@/components/documents/DocumentUpload';
import MainLayout from '@/components/layout/MainLayout';

export default function Documents() {
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
          <h1 className="text-3xl font-bold">Document Management</h1>
          <p className="text-muted-foreground mt-2">
            Upload and manage your study materials. The AI will analyze these documents to provide accurate answers.
          </p>
        </div>
        <DocumentUpload />
      </div>
    </MainLayout>
  );
} 