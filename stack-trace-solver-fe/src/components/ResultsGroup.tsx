import React from "react";
import { Row, Col, Button } from "react-bootstrap";
import ResultCard from "./ResultCard";
import InfoIcon from "../assets/info-icon.svg";
import Results from "../api/Results";

export interface IResultsGroupProps {
  results: Results;
  onBackButtonClick: () => void;
}

const ResultsGroup: React.FC<IResultsGroupProps> = (props: IResultsGroupProps) => {
  const renderResultCards = (): JSX.Element[] => {
    return props.results.results.map((result, index) => {
      return (
        <Row className="d-flex justify-content-center" key={index}>
          <Col className="mt-3" sm={8}>
            <ResultCard result={result} />
          </Col>
        </Row>
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
        {props.results.error &&  
          <h5 className="text-center m-2">Reason: {props.results.error}</h5>
        }
      </div>
    );
  };

  return (
    <Row className="mb-4 h-100 d-flex align-items-center justify-content-center">
      <Col>
        <Row>
          <Col>
            {props.results.results.length === 0 ? renderNoResultsInfoMessage() : renderResultCards()}
          </Col>
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

export default ResultsGroup;
