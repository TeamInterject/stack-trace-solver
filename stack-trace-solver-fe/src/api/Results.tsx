export default interface Results {
  results: Result[];
}

export interface Result {
  GeneratedQuery: string;
  DetectedException: string;
  Template: string;
  Link: string;
  Title: string;
  Score: number;
}
