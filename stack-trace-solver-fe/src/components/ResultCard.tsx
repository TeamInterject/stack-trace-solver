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
            <div>{props.result.Title.replace(/&quot;/g, "\"")}</div>
          </Card.Header>
          <Card.Body>
            <Card.Link href={props.result.Link} target="_blank">{props.result.Link}</Card.Link>
          </Card.Body>
          <Card.Footer>
              <div style={{ paddingBottom: "10px" }}><b>Dectected Exception: </b>{props.result.DetectedException}</div>
              <div style={{ paddingBottom: "10px" }}><b>Generated from Template: </b>{props.result.Template}</div>
              <div style={{ paddingBottom: "10px" }}><b>Generated Query: </b>{props.result.GeneratedQuery}</div>
          </Card.Footer>
        </Card>
      </Col>
    </Row>
  );
};

export default ResultCard;
