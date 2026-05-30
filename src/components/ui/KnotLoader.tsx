interface KnotLoaderProps {
  size?: 'sm' | 'md' | 'lg'
  className?: string
}

export default function KnotLoader({ size = 'md', className = '' }: KnotLoaderProps) {
  const sizeMap = { sm: 16, md: 32, lg: 48 }
  const s = sizeMap[size]

  return (
    <div className={`flex items-center justify-center ${className}`}>
      <div
        className="rounded-full border-[3px] border-border-default border-t-brand-blue animate-spin"
        style={{ width: s, height: s }}
      />
    </div>
  )
}
