import { ApiError } from '../auth/services/authApi';

export type Summary = {
  title: string;
  period: {
    start: string;
    end: string;
    label: string;
  };
  income_minor: number;
  expenses_minor: number;
  net_minor: number;
  savings_rate: number | null;
};

export type Message = {
  id: string;
  role: 'user' | 'assistant';
  content: string;
  created_at: string;
  request_id: string;
  summary: Summary | null;
};

export type ChatRequest = {
  id: string;
  content: string;
  status: 'pending' | 'failed' | 'completed';
  error_code: string | null;
  error_message: string | null;
  created_at: string;
};

export type Conversation = {
  id: string;
  title: string;
  updated_at: string;
};

export type History = {
  items: (Conversation & { preview: string })[];
  has_more: boolean;
  next_offset: number;
};

export type Detail = {
  conversation: Conversation;
  messages: Message[];
  request: ChatRequest | null;
  has_more: boolean;
  next_before: number | null;
};

export type SendResult = {
  messages: Message[];
  request: ChatRequest;
};

export type Status = {
  configured: boolean;
  connection_verified: boolean;
  message: string;
};

export class ChatError extends ApiError {
  constructor(
    message: string,
    status: number,
    public result?: SendResult,
    public code?: string
  ) {
    super(message, status);
  }
}

/**
 * API configuration:
 * - Production: uses the deployed FastAPI backend.
 * - Development: uses the Vite proxy when VITE_API_BASE_URL is empty.
 */
const DEFAULT_API_BASE_URL = 'https://fincept-ai-backend.onrender.com';

const configuredBaseUrl = (
  import.meta.env.VITE_API_BASE_URL || ''
).trim();

const base = configuredBaseUrl.replace(/\/+$/, '');

/**
 * Sends requests to the FINCEPT AI assistant API.
 *
 * Credentials are included to support the backend's HttpOnly
 * session cookies.
 */
export async function chatApi<T>(
  path: string,
  dataset: 'live' | 'demo',
  method = 'GET',
  body?: unknown,
  signal?: AbortSignal
): Promise<T> {
  let response: Response;

  const normalizedPath = path.startsWith('/') ? path : `/${path}`;

  const querySeparator = normalizedPath.includes('?') ? '&' : '?';

  const requestUrl = `${
    base || (import.meta.env.PROD ? DEFAULT_API_BASE_URL : '')
  }/api/assistant${normalizedPath}${querySeparator}dataset=${encodeURIComponent(dataset)}`;

  const headers: HeadersInit = {
    Accept: 'application/json',
  };

  if (method !== 'GET') {
    headers['Content-Type'] = 'application/json';
    headers['X-Fincept-Request'] = '1';
  }

  let timeoutSignal: AbortSignal;

  try {
    timeoutSignal = AbortSignal.timeout(40000);
  } catch {
    timeoutSignal = new AbortController().signal;
  }

  let combinedSignal: AbortSignal;

  if (signal) {
    combinedSignal =
      typeof AbortSignal.any === 'function'
        ? AbortSignal.any([signal, timeoutSignal])
        : signal;
  } else {
    combinedSignal = timeoutSignal;
  }

  try {
    response = await fetch(requestUrl, {
      method,
      credentials: 'include',
      headers,
      body: body === undefined ? undefined : JSON.stringify(body),
      signal: combinedSignal,
    });
  } catch (error) {
    if (signal?.aborted) {
      throw error;
    }

    throw new ChatError(
      'Connection interrupted. Check your network and try again. The same request ID will be reused.',
      0
    );
  }

  let data: any;

  try {
    data = await response.json();
  } catch {
    throw new ChatError(
      'Unable to read the assistant response. Please try again.',
      response.status
    );
  }

  if (signal?.aborted) {
    throw new DOMException('Request aborted', 'AbortError');
  }

  if (!response.ok) {
    throw new ChatError(
      data?.message || 'Unable to load the assistant. Please try again.',
      response.status,
      data?.request
        ? {
            ...data,
            messages: data.messages || [],
          }
        : undefined,
      data?.code
    );
  }

  return data as T;
}

export const questions = [
  {
    title: 'Understand my spending',
    question: 'Where did most of my money go this month?',
  },
  {
    title: 'Review my budget',
    question: 'Which of my budgets are close to their limits?',
  },
  {
    title: 'Savings goals',
    question: 'How much more do I need to save for my goals?',
  },
  {
    title: 'Cash flow',
    question: 'How much money did I have left this month?',
  },
];

/**
 * Conceals financial prose when privacy mode is enabled.
 * Stored messages and calculations remain unchanged.
 */
export function privateText(text: string, hidden: boolean): string {
  return hidden ? 'Message text hidden for monetary privacy.' : text;
}

/**
 * Merges messages by ID while preserving their existing order.
 */
export function mergeMessages(
  current: Message[],
  incoming: Message[]
): Message[] {
  const map = new Map(current.map((message) => [message.id, message]));

  for (const message of incoming) {
    map.set(message.id, message);
  }

  return Array.from(map.values());
}

/**
 * Formats timestamps for conversation history.
 */
export function readableTime(value: string): string {
  return new Date(value).toLocaleString('en-GB', {
    day: '2-digit',
    month: 'short',
    hour: '2-digit',
    minute: '2-digit',
  });
}