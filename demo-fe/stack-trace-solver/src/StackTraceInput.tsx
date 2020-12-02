import React from "react";
import { Col, Form, Row } from "react-bootstrap";

export interface IStackTraceInputProps {
  onSubmit: () => void;
}

const StackTraceInput: React.FC<IStackTraceInputProps> = (props: IStackTraceInputProps): JSX.Element => {
  const handleSubmit = (): void => {
    props.onSubmit();
  };

  return (
    <Row className="h-100 w-100">
      <Col className="my-auto align-middle">
        <Form onSubmit={handleSubmit} className="d-flex align-item-center justify-content-center">
        <h1>Insert stack trace...</h1>
        <Form.Control
          required
        />
        </Form>
      </Col>
    </Row>
  );
};

export default StackTraceInput;