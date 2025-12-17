export interface User {
  id: string;
  email: string;
  full_name: string;
  role: 'admin' | 'member';
  organization_id: string;
  is_active: boolean;
  created_at: string;
  last_login?: string;
}

export interface Organization {
  id: string;
  name: string;
  slug: string;
  tier: 'free' | 'pro' | 'enterprise';
  is_active: boolean;
  max_documents: number;
  max_storage_mb: number;
  max_users: number;
  current_documents: number;
  current_storage_mb: number;
  created_at: string;
}

export interface Document {
  id: string;
  organization_id: string;
  uploaded_by: string;
  filename: string;
  file_type: string;
  file_size: number;
  title: string;
  description?: string;
  status: 'uploading' | 'processing' | 'completed' | 'failed';
  error_message?: string;
  s3_key?: string;
  tags?: string[];
  created_at: string;
  updated_at: string;
}

export interface Conversation {
  id: string;
  organization_id: string;
  user_id: string;
  title: string;
  is_archived: boolean;
  created_at: string;
  updated_at: string;
  messages?: Message[];
}

export interface Message {
  id: string;
  conversation_id: string;
  role: 'user' | 'assistant';
  content: string;
  sources?: Source[];
  created_at: string;
}

export interface Source {
  document_id: string;
  document_title: string;
  chunk_text: string;
  score: number;
}

export interface ChatRequest {
  message: string;
  conversation_id?: string;
}

export interface ChatResponse {
  conversation_id: string;
  message: Message;
  sources: Source[];
}

export interface LoginRequest {
  email: string;
  password: string;
}

export interface RegisterRequest {
  email: string;
  password: string;
  full_name: string;
  organization_id?: string;
}

export interface TokenResponse {
  access_token: string;
  refresh_token: string;
  token_type: string;
}

export interface DocumentUpload {
  file: File;
  title?: string;
  description?: string;
}

export interface AnalyticsOverview {
  total_organizations: number;
  total_users: number;
  total_documents: number;
  total_conversations: number;
}

export interface UsageMetric {
  date: string;
  api_calls: number;
  documents_uploaded: number;
  chat_messages: number;
  total_cost: number;
}

