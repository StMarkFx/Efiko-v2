import { NextApiRequest, NextApiResponse } from 'next';
import { initializeApp } from 'firebase-admin/app';
import { getAuth } from 'firebase-admin/auth';

// Initialize Firebase Admin
const app = initializeApp({
  credential: process.env.FIREBASE_ADMIN_CREDENTIAL
    ? JSON.parse(process.env.FIREBASE_ADMIN_CREDENTIAL)
    : undefined
});

const auth = getAuth(app);

export default async function handler(
  req: NextApiRequest,
  res: NextApiResponse
) {
  if (req.method !== 'POST') {
    return res.status(405).json({ error: 'Method not allowed' });
  }

  try {
    const { email, password } = req.body;

    if (!email || !password) {
      return res.status(400).json({ error: 'Email and password are required' });
    }

    // Create user in Firebase
    const userRecord = await auth.createUser({
      email,
      password,
      emailVerified: false
    });

    return res.status(201).json({
      message: 'User created successfully',
      uid: userRecord.uid
    });
  } catch (error: any) {
    console.error('Registration error:', error);
    return res.status(500).json({
      error: error.message || 'Failed to create user'
    });
  }
} 