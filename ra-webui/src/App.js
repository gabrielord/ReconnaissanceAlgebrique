import { Box, Button, ChakraProvider, Flex, Spacer } from "@chakra-ui/react";

function App() {
  return (
    <ChakraProvider>
      <Flex flexDir="column" alignItems="center">
        <Box width="95vw" marginTop="30px">
          <Flex flexDir="row" gap="20px">
            <Box
              width="50%"
              height="750px"
              bgColor="gray.100"
              borderWidth="1px"
              borderColor="gray.200"
            >
              <Flex flexDir="column" width="100%">
                <Box
                  fontSize="2xl"
                  fontWeight="thin"
                  justifyContent="center"
                  textAlign="center"
                  width="100%"
                >
                  Reconnaissance Algebrique
                </Box>
              </Flex>
            </Box>
            <Box
              width="50%"
              height="750px"
              bgColor="gray.100"
              borderWidth="1px"
              borderColor="gray.200"
            ></Box>
          </Flex>
        </Box>

        <Box bgColor="grey" width="95vw">
          Debug display for different engines
        </Box>
      </Flex>
    </ChakraProvider>
  );
}

export default App;
