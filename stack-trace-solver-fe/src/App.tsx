import React, { useState } from 'react';
import { Col, Container, Row } from 'react-bootstrap';
import APIClient from './api/APIClient';
import './App.css';
import LoadingSpinner from './components/LoadingSpinner';
import ResultsGroup from './components/ResultsGroup';
import Results from './api/Results';
import StackTraceInput from './components/StackTraceInput';

function App() {
  const [isLoading, toggleIsLoading] = useState(false);
  const [showResultLinks, toggleShowResultLinks] = useState(false);
  const [results, setResults] = useState<Results>({} as Results);
  const client = new APIClient();

  const getPostedLinks = (stackTrace: string): void => {
    toggleIsLoading(true);
    client.getPostedLinks(stackTrace).then((resultsData) => {
      setResults(resultsData);
      toggleShowResultLinks(true);
      toggleIsLoading(false);
    }).catch((reason) => {
      toggleIsLoading(false);
      console.log(reason);
    });
  };

  return (
    <Container className="vh-100 d-flex flex-column">
      <LoadingSpinner isLoading={isLoading} />
      <Row className="mt-2 flex-fill">
        <Col>
          {showResultLinks
            ? 
            <ResultsGroup
              onBackButtonClick={() => toggleShowResultLinks(false)}
              results={results}
            />
            :
            <StackTraceInput onSubmit={getPostedLinks} />
          }
        </Col>
      </Row>
    </Container>
  );
}

export default App;
