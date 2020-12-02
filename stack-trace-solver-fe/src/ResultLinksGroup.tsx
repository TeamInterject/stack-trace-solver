import React from "react";
import { Row, Col, Button } from "react-bootstrap";
import ResultLinkCard from "./ResultLinkCard";

export interface IResultLinksGroupProps {
  links: string[];
  onBackButtonClick: () => void;
}

const ResultLinksGroup: React.FC<IResultLinksGroupProps> = (props: IResultLinksGroupProps) => {
  const renderResultLinkCards = (): JSX.Element[] => {
    return props.links.map((link, index) => {
      return (
        <Col className="mt-1" sm={3}>
          <ResultLinkCard title={`Result #${index}`} link={link} />
        </Col>
      );
    });
  };

  return (
    <Row className="h-100 d-flex align-items-center justify-content-center">
      <Col>
        <Row className="mt-2 d-flex justify-content-center">
          {renderResultLinkCards()}
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