import {
  Box,
  Button,
  ChakraProvider,
  Flex,
  Input,
  Select,
  Spacer,
} from "@chakra-ui/react";
import { useState } from "react";
import "katex/dist/katex.min.css";
import { BlockMath } from "react-katex";

function App() {
  const [leftExpr, setLeftExpr] = useState("");
  const [rightExpr, setRightExpr] = useState("");
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
              <Flex flexDir="column" width="100%" gap="20px">
                <Box
                  fontSize="2xl"
                  fontWeight="thin"
                  justifyContent="center"
                  textAlign="center"
                  width="100%"
                >
                  Reconnaissance Algebrique (hasn't been styled yet... todo)
                </Box>
                <Box
                  display="flex"
                  flexDir="row"
                  width="100%"
                  alignContents="center"
                >
                  <Box marginLeft="50px" marginRight="50px" textAlign="center">
                    Method
                  </Box>
                  <Select placeholder="Select option">
                    {" "}
                    {/**Get options from server */}
                    <option value="option1">Option 1</option>
                    <option value="option2">Option 2</option>
                    <option value="option3">Option 3</option>
                  </Select>
                </Box>

                <Box
                  display="flex"
                  flexDir="row"
                  width="100%"
                  alignContents="center"
                >
                  <Box
                    paddingLeft="50px"
                    paddingRight="50px"
                    alignContent="center"
                  >
                    Left Expression
                  </Box>
                  <Input
                    value={leftExpr}
                    onChange={(e) => setLeftExpr(e.target.value)}
                  />
                </Box>
                <Box
                  display="flex"
                  flexDir="row"
                  width="100%"
                  alignContents="center"
                >
                  <Box
                    paddingLeft="50px"
                    paddingRight="50px"
                    alignContent="center"
                  >
                    Right Expression
                  </Box>
                  <Input
                    value={rightExpr}
                    onChange={(e) => setRightExpr(e.target.value)}
                  />
                </Box>
                <Box fontWeight="bold">Preview</Box>
                <Box fontWeight="bold">Left expression : </Box>
                <Box>
                  <BlockMath>{leftExpr}</BlockMath>
                </Box>
                <Box fontWeight="bold">Right expression : </Box>
                <Box>
                  <BlockMath>{rightExpr}</BlockMath>
                </Box>
                <Button></Button>
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
