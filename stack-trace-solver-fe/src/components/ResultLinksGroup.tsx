import React from "react";
import { Row, Col, Button } from "react-bootstrap";
import ResultLinkCard from "./ResultLinkCard";
import InfoIcon from "../assets/info-icon.svg";
import Results from "../api/Results";

export interface IResultLinksGroupProps {
  results: Results;
  onBackButtonClick: () => void;
}

const ResultLinksGroup: React.FC<IResultLinksGroupProps> = (props: IResultLinksGroupProps) => {
  const renderResultLinkCards = (): JSX.Element[] => {
    return props.results.Results.map((result) => {
      return (
        <Col className="mt-3" sm={6}>
          <ResultLinkCard result={result} />
        </Col>
      );
    });
  };

  const renderNoResultsInfoMessage = (): JSX.Element => {
    return (
      <div className="h-100 d-flex flex-column align-items-center justify-content-center">
        <img src={InfoIcon} height="48px" width="48px" alt="Groups icon" />
        <h3 className="text-center m-2">
          No links were generated :/
        </h3>
      </div>
    );
  };

  return (
    <Row className="h-100 d-flex align-items-center justify-content-center">
      <Col>
        <Row className="mt-2 d-flex justify-content-center">
          {props.results.Results.length === 0 ? renderNoResultsInfoMessage() : renderResultLinkCards()}
        </Row>
        <Row>
          <Col className="mt-4 d-flex justify-content-center">
            <Button className="align-self-center" onClick={props.onBackButtonClick}>Try another stack trace</Button>
          </Col>
        </Row>
      </Col>
    </Row>
  );
};

export default ResultLinksGroup;