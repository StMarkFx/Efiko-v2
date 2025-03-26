import { ReactNode } from 'react';
import { ThemeProvider } from 'next-themes';
import Navbar from './Navbar';
import { Toaster } from '@/components/ui/toaster';

interface MainLayoutProps {
  children: ReactNode;
}

export default function MainLayout({ children }: MainLayoutProps) {
  return (
    <ThemeProvider attribute="class" defaultTheme="system" enableSystem>
      <div className="min-h-screen bg-background">
        <Navbar />
        <main className="container mx-auto px-4 py-8">
          {children}
        </main>
        <Toaster />
      </div>
    </ThemeProvider>
  );
} 