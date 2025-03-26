import { useTheme } from 'next-themes';
import { Moon, Sun } from 'lucide-react';
import { Button } from '@/components/ui/button';
import { useAuth } from '@/hooks/useAuth';

export default function Navbar() {
  const { theme, setTheme } = useTheme();
  const { user, signOut } = useAuth();

  return (
    <nav className="border-b">
      <div className="container mx-auto px-4 h-16 flex items-center justify-between">
        <div className="flex items-center space-x-4">
          <h1 className="text-xl font-bold">Efiko AI</h1>
          <div className="hidden md:flex space-x-4">
            <a href="/" className="hover:text-primary">Home</a>
            <a href="/chat" className="hover:text-primary">Chat</a>
            <a href="/documents" className="hover:text-primary">Documents</a>
          </div>
        </div>
        
        <div className="flex items-center space-x-4">
          <Button
            variant="ghost"
            size="icon"
            onClick={() => setTheme(theme === 'dark' ? 'light' : 'dark')}
          >
            {theme === 'dark' ? (
              <Sun className="h-5 w-5" />
            ) : (
              <Moon className="h-5 w-5" />
            )}
          </Button>
          
          {user ? (
            <div className="flex items-center space-x-4">
              <span className="text-sm">{user.email}</span>
              <Button variant="outline" onClick={signOut}>
                Sign Out
              </Button>
            </div>
          ) : (
            <Button variant="default" onClick={() => window.location.href = '/login'}>
              Sign In
            </Button>
          )}
        </div>
      </div>
    </nav>
  );
} 