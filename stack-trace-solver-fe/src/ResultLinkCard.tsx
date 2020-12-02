import React from "react";
import { Card, Col, Row } from "react-bootstrap";

export interface IResultLinkCardProps {
  title: string;
  link: string;
}

const ResultLinkCard: React.FC<IResultLinkCardProps> = (props: IResultLinkCardProps): JSX.Element => {
  return (
    <Row>
      <Col>
        <Card className="shadow rounded">
          <Card.Header as="h5">{props.title}</Card.Header>
          <Card.Body>
            <Card.Link href="#">{props.link}</Card.Link>
          </Card.Body>
        </Card>
      </Col>
    </Row>
  );
};

export default ResultLinkCard;