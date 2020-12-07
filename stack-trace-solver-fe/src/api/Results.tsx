export default interface Results {
  results: Result[];
  error?: string;
}

export interface Result {
  GeneratedQuery: string;
  DetectedException: string;
  Template: string;
  Link: string;
  Title: string;
  Score: number;
}
