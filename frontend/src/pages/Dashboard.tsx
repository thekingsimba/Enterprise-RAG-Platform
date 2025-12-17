import React from 'react';
import {
  Box,
  Container,
  Heading,
  SimpleGrid,
  Stat,
  StatLabel,
  StatNumber,
  StatHelpText,
  useColorModeValue,
  Text,
  VStack,
} from '@chakra-ui/react';
import { useAuth } from '@/contexts/AuthContext';
import { useDocuments } from '@/hooks/useDocuments';
import { useConversations } from '@/hooks/useChat';

const Dashboard: React.FC = () => {
  const { user } = useAuth();
  const { data: documents } = useDocuments(0, 100);
  const { data: conversations } = useConversations(0, 100);

  const cardBg = useColorModeValue('white', 'gray.700');

  return (
    <Container maxW="container.xl" py={8}>
      <VStack align="stretch" spacing={8}>
        <Box>
          <Heading size="lg" mb={2}>
            Welcome back, {user?.full_name}!
          </Heading>
          <Text color="gray.600">
            Here's an overview of your RAG platform activity
          </Text>
        </Box>

        <SimpleGrid columns={{ base: 1, md: 3 }} spacing={6}>
          <Box
            bg={cardBg}
            p={6}
            borderRadius="lg"
            shadow="md"
            borderWidth="1px"
          >
            <Stat>
              <StatLabel>Total Documents</StatLabel>
              <StatNumber>{documents?.length || 0}</StatNumber>
              <StatHelpText>Uploaded documents</StatHelpText>
            </Stat>
          </Box>

          <Box
            bg={cardBg}
            p={6}
            borderRadius="lg"
            shadow="md"
            borderWidth="1px"
          >
            <Stat>
              <StatLabel>Conversations</StatLabel>
              <StatNumber>{conversations?.length || 0}</StatNumber>
              <StatHelpText>Chat sessions</StatHelpText>
            </Stat>
          </Box>

          <Box
            bg={cardBg}
            p={6}
            borderRadius="lg"
            shadow="md"
            borderWidth="1px"
          >
            <Stat>
              <StatLabel>User Role</StatLabel>
              <StatNumber textTransform="capitalize">{user?.role}</StatNumber>
              <StatHelpText>Your access level</StatHelpText>
            </Stat>
          </Box>
        </SimpleGrid>

        <Box
          bg={cardBg}
          p={6}
          borderRadius="lg"
          shadow="md"
          borderWidth="1px"
        >
          <Heading size="md" mb={4}>
            Quick Start
          </Heading>
          <VStack align="stretch" spacing={3}>
            <Text>
              📄 <strong>Upload Documents:</strong> Go to the Documents page to upload your files
            </Text>
            <Text>
              💬 <strong>Start Chatting:</strong> Use the Chat page to ask questions about your documents
            </Text>
            <Text>
              🔍 <strong>RAG-Powered:</strong> Get accurate answers with sources from your uploaded content
            </Text>
          </VStack>
        </Box>
      </VStack>
    </Container>
  );
};

export default Dashboard;

