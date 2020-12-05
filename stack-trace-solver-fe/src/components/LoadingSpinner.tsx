import React from "react";
import Loader from "react-loader-spinner";
import "../loading-spinner.css";

export interface ILoadingSpinnerProps {
  isLoading: boolean;
}

export default class LoadingSpinner extends React.Component<ILoadingSpinnerProps> {
  render(): JSX.Element {
    const { isLoading } = this.props;

    return (
      <div className={isLoading ? "loading-spinner-container" : "loading-spinner-container--disabled"}>
        <div className="loading-spinner-container__spinner">
          <Loader type="Oval" color="#007aff" height={100} width={100} />
        </div>
      </div>
    );
  }
}