import React, { useState } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import './App.css';
import LoadingSpinner from './LoadingSpinner';
import ResultLinksGroup from './ResultLinksGroup';
import StackTraceInput from './StackTraceInput';

function App() {
  const [isLoading, toggleIsLoading] = useState(false);
  const [showResultLinks, toggleShowResultLinks] = useState(false);

  return (
    <Container className="vh-100 mt-2 d-flex flex-column">
      <LoadingSpinner isLoading={isLoading} />
      <Row className="flex-fill">
        <Col>
          {showResultLinks 
            ? 
            <ResultLinksGroup
              onBackButtonClick={() => toggleShowResultLinks(false)}
              links={["www.google.com", "www.github.com"]}
            />
            :
            <StackTraceInput onSubmit={() => {toggleShowResultLinks(true)}} />
          }
        </Col>
      </Row>
    </Container>
  );
}

export default App;
