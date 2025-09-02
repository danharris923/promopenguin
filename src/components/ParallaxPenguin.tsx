import React, { useEffect, useState } from 'react';

interface ParallaxPenguinProps {
  className?: string;
  scale?: number;
  opacity?: number;
}

const ParallaxPenguin: React.FC<ParallaxPenguinProps> = ({ 
  className = '', 
  scale = 1,
  opacity = 0.1 
}) => {
  const [scrollY, setScrollY] = useState(0);

  useEffect(() => {
    const handleScroll = () => {
      setScrollY(window.scrollY);
    };

    window.addEventListener('scroll', handleScroll);
    return () => window.removeEventListener('scroll', handleScroll);
  }, []);

  // Calculate parallax offset (slower than normal scroll)
  const parallaxOffset = scrollY * 0.3;

  return (
    <div 
      className={`fixed pointer-events-none select-none z-0 ${className}`}
      style={{
        transform: `translateY(${parallaxOffset}px) scale(${scale})`,
        opacity: opacity,
        transition: 'opacity 0.3s ease-out'
      }}
    >
      <img 
        src="/promopenguin.png" 
        alt="PromoPenguin" 
        className="w-full h-full object-contain"
        draggable={false}
      />
    </div>
  );
};

export default ParallaxPenguin;