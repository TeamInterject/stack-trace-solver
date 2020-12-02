import React, { useState } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import './App.css';
import LoadingSpinner from './LoadingSpinner';
import StackTraceInput from './StackTraceInput';

function App() {
  const [isLoading, toggleIsLoading] = useState(false);

  return (
    <Container className="vh-100 mt-2 d-flex flex-column">
      <LoadingSpinner isLoading={isLoading} />
      <Row className="flex-fill">
        <Col>
          <StackTraceInput onSubmit={() => {}} />
        </Col>
      </Row>
    </Container>
  );
}

export default App;
