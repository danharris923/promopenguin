import React, { useEffect } from 'react';
import { motion, PanInfo, useMotionValue, useTransform } from 'framer-motion';
import { Deal } from '../types/Deal';

interface BottomSheetProps {
  deal: Deal | null;
  isOpen: boolean;
  onClose: () => void;
}

const BottomSheet: React.FC<BottomSheetProps> = ({ deal, isOpen, onClose }) => {
  const y = useMotionValue(0);
  const opacity = useTransform(y, [0, 300], [1, 0]);

  useEffect(() => {
    if (isOpen) {
      // Prevent body scroll when bottom sheet is open
      document.body.style.overflow = 'hidden';
    } else {
      document.body.style.overflow = 'unset';
    }

    return () => {
      document.body.style.overflow = 'unset';
    };
  }, [isOpen]);

  if (!isOpen || !deal) return null;

  const handleDragEnd = (event: MouseEvent | TouchEvent | PointerEvent, info: PanInfo) => {
    // More sensitive swipe detection for better UX
    if (info.offset.y > 100 || info.velocity.y > 300) {
      onClose();
    }
  };

  const handleBackdropClick = (e: React.MouseEvent) => {
    if (e.target === e.currentTarget) {
      onClose();
    }
  };

  return (
    <>
      {/* Backdrop */}
      <motion.div
        className="fixed inset-0 bg-black/40 z-50 lg:hidden"
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        exit={{ opacity: 0 }}
        onClick={handleBackdropClick}
        style={{ opacity }}
      />

      {/* Bottom Sheet */}
      <motion.div
        className="fixed bottom-0 left-0 right-0 bg-penguin-charcoal border-t border-penguin-gray rounded-t-3xl z-50 max-h-[85vh] overflow-hidden lg:hidden"
        style={{ y }}
        initial={{ y: '100%' }}
        animate={{ y: 0 }}
        exit={{ y: '100%' }}
        transition={{
          type: 'spring',
          damping: 30,
          stiffness: 300,
          mass: 0.8, // iOS-style spring physics
        }}
        drag="y"
        dragConstraints={{ top: 0, bottom: 0 }}
        dragElastic={0.1}
        onDragEnd={handleDragEnd}
      >
        {/* Drag Handle */}
        <div className="flex justify-center pt-4 pb-3">
          <div className="w-12 h-1.5 bg-penguin-gray rounded-full transition-colors duration-200 hover:bg-gray-400" />
        </div>

        {/* Content */}
        <div className="px-6 pb-8 overflow-y-auto max-h-[calc(85vh-60px)]">
          {/* Product Image */}
          <div className="flex justify-center mb-6">
            <div className="relative w-48 h-48 bg-penguin-dark-gray rounded-2xl overflow-hidden">
              <img
                src={deal.imageUrl}
                alt={deal.title}
                className="w-full h-full object-contain p-4"
                onError={(e) => {
                  e.currentTarget.src = '/placeholder-deal.svg';
                }}
              />
            </div>
          </div>

          {/* Product Title */}
          <h2 className="text-xl font-bold text-penguin-white mb-4 leading-tight">
            {deal.title}
          </h2>

          {/* Description */}
          <div className="mb-6">
            <p className="text-penguin-white leading-relaxed">
              {deal.description}
            </p>
          </div>

          {/* Action Button */}
          <div className="space-y-3">
            <a
              href={deal.affiliateUrl}
              target="_blank"
              rel="noopener noreferrer"
              className="block w-full bg-gradient-to-r from-penguin-ice-blue to-blue-400 text-penguin-black text-center py-4 px-6 rounded-2xl font-bold text-lg shadow-lg active:scale-95 transition-all duration-150"
            >
              🛒 Shop This Deal
            </a>

            {/* Secondary Info */}
            <div className="text-center">
              <p className="text-xs text-gray-400">
                Deal added on {new Date(deal.dateAdded).toLocaleDateString()}
              </p>
            </div>
          </div>
        </div>
      </motion.div>
    </>
  );
};

export default BottomSheet;