import { Deal } from './Deal';

export interface Store {
  id: string;
  name: string;
  logo?: string;
  deals: Deal[];
  totalDeals: number;
  averageDiscount: number;
  maxDiscount: number;
  previewImage: string;
  category?: string;
}