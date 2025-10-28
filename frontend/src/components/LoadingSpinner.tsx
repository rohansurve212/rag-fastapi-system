/**
 * LoadingSpinner Component
 * 
 * Reusable loading spinner with optional text
 */

import { Loader2 } from 'lucide-react';
import { cn } from '@/utils';

interface LoadingSpinnerProps {
  size?: 'sm' | 'md' | 'lg';
  text?: string;
  className?: string;
}

const sizeClasses = {
  sm: 'w-4 h-4',
  md: 'w-8 h-8',
  lg: 'w-12 h-12',
};

const LoadingSpinner: React.FC<LoadingSpinnerProps> = ({
  size = 'md',
  text,
  className,
}) => {
  return (
    <div className={cn('flex flex-col items-center justify-center', className)}>
      <Loader2 className={cn(sizeClasses[size], 'animate-spin text-primary-600')} />
      {text && <p className="mt-3 text-sm text-gray-600">{text}</p>}
    </div>
  );
};

export default LoadingSpinner;
