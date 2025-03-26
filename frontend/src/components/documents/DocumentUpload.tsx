import { useState, useCallback } from 'react';
import { useDropzone } from 'react-dropzone';
import { Button } from '@/components/ui/button';
import { useToast } from '@/components/ui/use-toast';
import { useAuth } from '@/hooks/useAuth';
import { Upload, File, X } from 'lucide-react';

interface UploadedFile {
  file: File;
  progress: number;
  status: 'uploading' | 'completed' | 'error';
}

export default function DocumentUpload() {
  const [uploadedFiles, setUploadedFiles] = useState<UploadedFile[]>([]);
  const { toast } = useToast();
  const { user } = useAuth();

  const onDrop = useCallback(async (acceptedFiles: File[]) => {
    if (!user) {
      toast({
        title: 'Error',
        description: 'Please sign in to upload documents.',
        variant: 'destructive'
      });
      return;
    }

    const newFiles: UploadedFile[] = acceptedFiles.map(file => ({
      file,
      progress: 0,
      status: 'uploading' as const
    }));

    setUploadedFiles(prev => [...prev, ...newFiles]);

    for (const fileData of newFiles) {
      try {
        const formData = new FormData();
        formData.append('file', fileData.file);

        const response = await fetch('/api/documents/upload', {
          method: 'POST',
          headers: {
            'Authorization': `Bearer ${await user.getIdToken()}`
          },
          body: formData
        });

        if (!response.ok) {
          throw new Error('Upload failed');
        }

        setUploadedFiles(prev =>
          prev.map(f =>
            f.file === fileData.file
              ? { ...f, progress: 100, status: 'completed' as const }
              : f
          )
        );

        toast({
          title: 'Success',
          description: `${fileData.file.name} uploaded successfully.`
        });
      } catch (error) {
        setUploadedFiles(prev =>
          prev.map(f =>
            f.file === fileData.file
              ? { ...f, status: 'error' as const }
              : f
          )
        );

        toast({
          title: 'Error',
          description: `Failed to upload ${fileData.file.name}.`,
          variant: 'destructive'
        });
      }
    }
  }, [user, toast]);

  const { getRootProps, getInputProps, isDragActive } = useDropzone({
    onDrop,
    accept: {
      'application/pdf': ['.pdf'],
      'application/msword': ['.doc'],
      'application/vnd.openxmlformats-officedocument.wordprocessingml.document': ['.docx']
    }
  });

  const removeFile = (fileToRemove: File) => {
    setUploadedFiles(prev =>
      prev.filter(file => file.file !== fileToRemove)
    );
  };

  return (
    <div className="space-y-4">
      <div
        {...getRootProps()}
        className={`border-2 border-dashed rounded-lg p-8 text-center cursor-pointer transition-colors
          ${isDragActive ? 'border-primary bg-primary/5' : 'border-muted-foreground/25'}`}
      >
        <input {...getInputProps()} />
        <Upload className="mx-auto h-12 w-12 text-muted-foreground" />
        <p className="mt-2 text-sm text-muted-foreground">
          {isDragActive
            ? 'Drop the files here'
            : 'Drag and drop files here, or click to select files'}
        </p>
        <p className="text-xs text-muted-foreground mt-1">
          Supported formats: PDF, DOC, DOCX
        </p>
      </div>

      {uploadedFiles.length > 0 && (
        <div className="space-y-2">
          <h3 className="text-sm font-medium">Uploaded Files</h3>
          <div className="space-y-2">
            {uploadedFiles.map((fileData, index) => (
              <div
                key={index}
                className="flex items-center justify-between p-2 rounded-lg bg-muted"
              >
                <div className="flex items-center space-x-2">
                  <File className="h-4 w-4" />
                  <span className="text-sm">{fileData.file.name}</span>
                </div>
                <div className="flex items-center space-x-2">
                  {fileData.status === 'uploading' && (
                    <div className="w-20 h-1 bg-muted-foreground/20 rounded-full overflow-hidden">
                      <div
                        className="h-full bg-primary transition-all duration-300"
                        style={{ width: `${fileData.progress}%` }}
                      />
                    </div>
                  )}
                  {fileData.status === 'completed' && (
                    <span className="text-xs text-green-500">Completed</span>
                  )}
                  {fileData.status === 'error' && (
                    <span className="text-xs text-red-500">Error</span>
                  )}
                  <Button
                    variant="ghost"
                    size="icon"
                    onClick={() => removeFile(fileData.file)}
                  >
                    <X className="h-4 w-4" />
                  </Button>
                </div>
              </div>
            ))}
          </div>
        </div>
      )}
    </div>
  );
} 