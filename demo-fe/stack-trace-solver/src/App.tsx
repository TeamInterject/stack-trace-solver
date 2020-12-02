import React from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import './App.css';
import StackTraceInput from './StackTraceInput';

function App() {
  return (
    <Container className="vh-100 vw-100 ml-20">
      <Row>
        <Col className="justify-content-center align-items-center ml-20">
          <StackTraceInput onSubmit={() => {}} />
        </Col>
      </Row>
    </Container>
  );
}

export default App;
