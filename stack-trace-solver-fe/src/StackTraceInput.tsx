import React, { useState } from "react";
import { Col, Form, Row, Button } from "react-bootstrap";

export interface IStackTraceInputProps {
  onSubmit: (stackTrace: string) => void;
}

const StackTraceInput: React.FC<IStackTraceInputProps> = (props: IStackTraceInputProps): JSX.Element => {
  const [stackTrace, setStackTrace] = useState(""); 

  const handleSubmit = (): void => {
    props.onSubmit(stackTrace);
  };

  const handleChange = (event: React.ChangeEvent<HTMLInputElement>): void => {
    setStackTrace(event.target.value);
  };

  return (
    <Row className="d-flex align-items-center justify-content-center">
      <Col>
        <Form onSubmit={handleSubmit}>
          <Form.Row>
            <h1>Insert stack trace...</h1>
          </Form.Row>
          <Form.Row>
            <Form.Control
              required
              as="textarea"
              rows={20}
              value={stackTrace}
              onChange={handleChange}
            />
          </Form.Row>
          <Form.Row className="mt-2 justify-content-end">
            <Button type="submit" size="lg">Solve it!</Button>
          </Form.Row>
        </Form>
      </Col>
    </Row>
  );
};

export default StackTraceInput;