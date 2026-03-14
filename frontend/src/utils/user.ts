import type { User } from '../types';

export const formatUserDisplayName = (user?: Partial<User> | null) => {
  if (!user) return '';
  if (user.role === 'admin') return 'Admin';

  const parts = [user.first_name?.trim(), user.last_name?.trim()].filter(Boolean);
  return parts.join(' ') || user.username || '';
};
