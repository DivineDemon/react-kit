declare type Item = {
  id: number;
  name: string;
  image_url: string;
  description: string;
};

declare type GlobalState = {
  token: string | null;
  profile_picture: string | null;
};

declare type HealthCheck = {
  status: string;
  message: string;
};