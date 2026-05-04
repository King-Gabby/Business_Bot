export interface Message {
  id: string;
  sender: 'user' | 'bot';
  text: string;
  timestamp: number;
}

export interface ChatResponse {
  reply: string;
  options: string[];
  state: {
    stage: string;
    selected_product: string | null;
    quantity: number | null;
    mode: 'bot' | 'human';
    fallback_count: number;
  };
  card?: {
    type: 'product_grid' | 'product_detail';
    items?: Array<{ name: string; price: string }>;
    name?: string;
    price?: string;
  } | null;
  ui?: {
    show_input: boolean;
    lock_input: boolean;
  };
}
