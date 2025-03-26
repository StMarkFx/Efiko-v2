import { Button } from '@/components/ui/button';
import { useAuth } from '@/hooks/useAuth';
import { ArrowRight, Brain, FileText, MessageSquare } from 'lucide-react';

export default function Home() {
  const { user } = useAuth();

  return (
    <div className="space-y-16">
      {/* Hero Section */}
      <section className="text-center space-y-6 py-20">
        <h1 className="text-4xl font-bold tracking-tight sm:text-6xl">
          Your AI-Powered Study Assistant
        </h1>
        <p className="text-xl text-muted-foreground max-w-2xl mx-auto">
          Upload your study materials and get instant answers to your questions. Powered by advanced AI and RAG technology.
        </p>
        <div className="flex justify-center gap-4">
          {user ? (
            <Button size="lg" onClick={() => window.location.href = '/chat'}>
              Start Chatting <ArrowRight className="ml-2 h-4 w-4" />
            </Button>
          ) : (
            <Button size="lg" onClick={() => window.location.href = '/login'}>
              Get Started
            </Button>
          )}
        </div>
      </section>

      {/* Features Section */}
      <section className="grid grid-cols-1 md:grid-cols-3 gap-8">
        <div className="space-y-4 text-center">
          <div className="mx-auto w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
            <Brain className="h-6 w-6 text-primary" />
          </div>
          <h3 className="text-xl font-semibold">AI-Powered Responses</h3>
          <p className="text-muted-foreground">
            Get accurate and contextual answers based on your study materials.
          </p>
        </div>

        <div className="space-y-4 text-center">
          <div className="mx-auto w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
            <FileText className="h-6 w-6 text-primary" />
          </div>
          <h3 className="text-xl font-semibold">Document Upload</h3>
          <p className="text-muted-foreground">
            Upload your PDFs, DOCs, and other study materials for instant access.
          </p>
        </div>

        <div className="space-y-4 text-center">
          <div className="mx-auto w-12 h-12 rounded-full bg-primary/10 flex items-center justify-center">
            <MessageSquare className="h-6 w-6 text-primary" />
          </div>
          <h3 className="text-xl font-semibold">Interactive Chat</h3>
          <p className="text-muted-foreground">
            Have natural conversations with AI about your study materials.
          </p>
        </div>
      </section>

      {/* How It Works Section */}
      <section className="space-y-8">
        <h2 className="text-3xl font-bold text-center">How It Works</h2>
        <div className="grid grid-cols-1 md:grid-cols-4 gap-8">
          <div className="space-y-2 text-center">
            <div className="mx-auto w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center">
              1
            </div>
            <p className="font-medium">Upload Documents</p>
          </div>
          <div className="space-y-2 text-center">
            <div className="mx-auto w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center">
              2
            </div>
            <p className="font-medium">Process & Index</p>
          </div>
          <div className="space-y-2 text-center">
            <div className="mx-auto w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center">
              3
            </div>
            <p className="font-medium">Ask Questions</p>
          </div>
          <div className="space-y-2 text-center">
            <div className="mx-auto w-8 h-8 rounded-full bg-primary text-primary-foreground flex items-center justify-center">
              4
            </div>
            <p className="font-medium">Get Answers</p>
          </div>
        </div>
      </section>
    </div>
  );
} 