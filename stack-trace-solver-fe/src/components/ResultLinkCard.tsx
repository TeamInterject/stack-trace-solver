import React from "react";
import { Card, Col, Row } from "react-bootstrap";
import { Result } from "../api/Results";

export interface IResultLinkCardProps {
  result: Result;
}

const ResultLinkCard: React.FC<IResultLinkCardProps> = (props: IResultLinkCardProps): JSX.Element => {
  return (
    <Row>
      <Col>
        <Card className="shadow rounded">
          <Card.Header as="h5">{props.result.Title}</Card.Header>
          <Card.Body>
            <Card.Link href="#">{props.result.Link}</Card.Link>
          </Card.Body>
        </Card>
      </Col>
    </Row>
  );
};

export default ResultLinkCard;