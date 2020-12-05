import Axios, { AxiosResponse } from "axios";
import Results from "./Results";

export default class APIClient {

  private BASE_URL = "http://127.0.0.1:5000/";
  
  public getPostedLinks = async (stackTrace: string): Promise<Results> => {
    return Axios.post(this.BASE_URL, { stack: stackTrace }).then((response: AxiosResponse<Results>) => {
      return response.data;
    });
  };
}