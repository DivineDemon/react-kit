declare type Item = {
  id: number;
  name: string;
  image_url: string;
  description: string;
};

declare type GlobalState = {
  item: Item | null;
  token: string | null;
};

declare type HealthCheck = {
  status: string;
  message: string;
};