import { NextApiRequest, NextApiResponse } from 'next';
import { initializeApp } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';
import formidable from 'formidable';
import fs from 'fs';

// Initialize Firebase Admin
const app = initializeApp({
  credential: process.env.FIREBASE_ADMIN_CREDENTIAL
    ? JSON.parse(process.env.FIREBASE_ADMIN_CREDENTIAL)
    : undefined
});

const auth = getAuth(app);

export const config = {
  api: {
    bodyParser: false,
  },
};

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    // Verify Firebase token
    const authHeader = req.headers.authorization;
    if (!authHeader?.startsWith('Bearer ')) {
      return res.status(401).json({ error: 'Unauthorized' });
    }

    const token = authHeader.split('Bearer ')[1];
    const decodedToken = await auth.verifyIdToken(token);
    const userId = decodedToken.uid;

    // Parse form data
    const form = formidable({
      maxFileSize: 10 * 1024 * 1024, // 10MB limit
      filter: (part) => {
        return (
          part.mimetype === 'application/pdf' ||
          part.mimetype === 'application/msword' ||
          part.mimetype === 'application/vnd.openxmlformats-officedocument.wordprocessingml.document'
        );
      },
    });

    const [fields, files] = await new Promise((resolve, reject) => {
      form.parse(req, (err, fields, files) => {
        if (err) reject(err);
        resolve([fields, files]);
      });
    });

    const file = files.file?.[0];
    if (!file) {
      return res.status(400).json({ error: 'No file uploaded' });
    }

    // Read file content
    const fileContent = fs.readFileSync(file.filepath, 'utf-8');

    // Forward request to backend
    const response = await fetch(`${process.env.BACKEND_URL}/api/documents/upload`, {
      method: 'POST',
      headers: {
        'Content-Type': 'application/json',
        'Authorization': `Bearer ${token}`
      },
      body: JSON.stringify({
        content: fileContent,
        filename: file.originalFilename,
        mimetype: file.mimetype,
        userId
      })
    });

    if (!response.ok) {
      throw new Error('Backend request failed');
    }

    const data = await response.json();
    return res.status(200).json(data);
  } catch (error: any) {
    console.error('Upload error:', error);
    return res.status(500).json({
      error: error.message || 'Failed to upload document'
    });
  }
} 