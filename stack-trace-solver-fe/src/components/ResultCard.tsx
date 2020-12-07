import React from "react";
import { Card, Col, Row } from "react-bootstrap";
import { Result } from "../api/Results";

export interface IResultCardProps {
  result: Result;
}

const ResultCard: React.FC<IResultCardProps> = (props: IResultCardProps): JSX.Element => {
  return (
    <Row>
      <Col>
        <Card className="shadow rounded">
          <Card.Header>
            <div style={{ fontWeight: "bold" }}>Score: {props.result.Score}</div>
            <div>{props.result.Title.replace(/&quot;/g, "\"").replace(/&#39;/g, "'")}</div>
          </Card.Header>
          <Card.Body>
            <Card.Link href={props.result.Link} target="_blank">{props.result.Link}</Card.Link>
          </Card.Body>
        </Card>
      </Col>
    </Row>
  );
};

export default ResultCard;
