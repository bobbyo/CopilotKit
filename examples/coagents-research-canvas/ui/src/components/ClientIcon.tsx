'use client';

import { useEffect, useState } from 'react';

/**
 * Wrapper to render icons client-side only, preventing hydration mismatches.
 * Icons won't appear in SSR HTML but will render immediately on client mount.
 */
export function ClientIcon({ children }: { children: React.ReactNode }) {
  const [mounted, setMounted] = useState(false);

  useEffect(() => {
    setMounted(true);
  }, []);

  // Return null during SSR, render icon after mount
  return mounted ? <>{children}</> : null;
}
