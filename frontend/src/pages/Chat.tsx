import React, { useState, useRef, useEffect } from 'react';
import {
  Box,
  Container,
  HStack,
  VStack,
  Input,
  Button,
  Text,
  useColorModeValue,
  Avatar,
  Flex,
  Spinner,
  Badge,
  Accordion,
  AccordionItem,
  AccordionButton,
  AccordionPanel,
  AccordionIcon,
  Divider,
  IconButton,
  Menu,
  MenuButton,
  MenuList,
  MenuItem,
} from '@chakra-ui/react';
import { ChatIcon, DeleteIcon } from '@chakra-ui/icons';
import { useConversations, useSendMessage, useDeleteConversation } from '@/hooks/useChat';
import { useAuth } from '@/contexts/AuthContext';
import { Message, Source } from '@/types';

const Chat: React.FC = () => {
  const { user } = useAuth();
  const { data: conversations } = useConversations();
  const sendMessageMutation = useSendMessage();
  const deleteConversationMutation = useDeleteConversation();

  const [selectedConversationId, setSelectedConversationId] = useState<string | null>(null);
  const [messages, setMessages] = useState<Message[]>([]);
  const [inputMessage, setInputMessage] = useState('');
  const [isTyping, setIsTyping] = useState(false);
  const messagesEndRef = useRef<HTMLDivElement>(null);

  const bgColor = useColorModeValue('white', 'gray.700');
  const inputBg = useColorModeValue('gray.50', 'gray.600');

  const scrollToBottom = () => {
    messagesEndRef.current?.scrollIntoView({ behavior: 'smooth' });
  };

  useEffect(() => {
    scrollToBottom();
  }, [messages]);

  const handleSendMessage = async () => {
    if (!inputMessage.trim()) return;

    const userMessage: Message = {
      id: Date.now().toString(),
      conversation_id: selectedConversationId || '',
      role: 'user',
      content: inputMessage,
      created_at: new Date().toISOString(),
    };

    setMessages((prev) => [...prev, userMessage]);
    setInputMessage('');
    setIsTyping(true);

    try {
      const response = await sendMessageMutation.mutateAsync({
        message: inputMessage,
        conversation_id: selectedConversationId || undefined,
      });

      if (!selectedConversationId) {
        setSelectedConversationId(response.conversation_id);
      }

      setMessages((prev) => [...prev, response.message]);
    } catch (error) {
      console.error('Failed to send message:', error);
    } finally {
      setIsTyping(false);
    }
  };

  const handleKeyPress = (e: React.KeyboardEvent) => {
    if (e.key === 'Enter' && !e.shiftKey) {
      e.preventDefault();
      handleSendMessage();
    }
  };

  const handleNewChat = () => {
    setSelectedConversationId(null);
    setMessages([]);
  };

  const handleSelectConversation = (conversationId: string) => {
    const conversation = conversations?.find((c) => c.id === conversationId);
    if (conversation) {
      setSelectedConversationId(conversationId);
      setMessages(conversation.messages || []);
    }
  };

  const handleDeleteConversation = async (conversationId: string) => {
    if (window.confirm('Are you sure you want to delete this conversation?')) {
      await deleteConversationMutation.mutateAsync(conversationId);
      if (selectedConversationId === conversationId) {
        handleNewChat();
      }
    }
  };

  return (
    <Container maxW="container.xl" py={8} h="calc(100vh - 100px)">
      <HStack spacing={4} h="full" align="stretch">
        {/* Conversations Sidebar */}
        <Box
          w="300px"
          bg={bgColor}
          borderRadius="lg"
          shadow="md"
          borderWidth="1px"
          p={4}
          display={{ base: 'none', md: 'block' }}
        >
          <VStack align="stretch" spacing={4}>
            <Button leftIcon={<ChatIcon />} colorScheme="blue" onClick={handleNewChat}>
              New Chat
            </Button>
            <Divider />
            <VStack align="stretch" spacing={2} overflowY="auto" maxH="calc(100vh - 250px)">
              {conversations?.map((conv) => (
                <HStack
                  key={conv.id}
                  p={3}
                  borderRadius="md"
                  cursor="pointer"
                  bg={selectedConversationId === conv.id ? 'blue.50' : 'transparent'}
                  _hover={{ bg: 'gray.50' }}
                  onClick={() => handleSelectConversation(conv.id)}
                  justify="space-between"
                >
                  <Text fontSize="sm" noOfLines={1} flex={1}>
                    {conv.title}
                  </Text>
                  <IconButton
                    aria-label="Delete"
                    icon={<DeleteIcon />}
                    size="xs"
                    variant="ghost"
                    onClick={(e) => {
                      e.stopPropagation();
                      handleDeleteConversation(conv.id);
                    }}
                  />
                </HStack>
              ))}
            </VStack>
          </VStack>
        </Box>

        {/* Chat Area */}
        <VStack flex={1} spacing={0} h="full">
          <Box
            flex={1}
            w="full"
            bg={bgColor}
            borderRadius="lg"
            shadow="md"
            borderWidth="1px"
            p={6}
            overflowY="auto"
          >
            {messages.length === 0 ? (
              <Flex h="full" align="center" justify="center" direction="column">
                <ChatIcon boxSize={12} color="gray.300" mb={4} />
                <Text color="gray.500" textAlign="center">
                  Start a conversation by typing a message below
                </Text>
              </Flex>
            ) : (
              <VStack align="stretch" spacing={4}>
                {messages.map((message, index) => (
                  <MessageBubble
                    key={message.id || index}
                    message={message}
                    isUser={message.role === 'user'}
                    userName={user?.full_name}
                  />
                ))}
                {isTyping && (
                  <HStack>
                    <Avatar size="sm" name="AI" />
                    <Box bg="gray.100" p={3} borderRadius="lg">
                      <HStack spacing={1}>
                        <Spinner size="xs" />
                        <Text fontSize="sm">Thinking...</Text>
                      </HStack>
                    </Box>
                  </HStack>
                )}
                <div ref={messagesEndRef} />
              </VStack>
            )}
          </Box>

          {/* Input Area */}
          <Box w="full" mt={4}>
            <HStack>
              <Input
                value={inputMessage}
                onChange={(e) => setInputMessage(e.target.value)}
                onKeyPress={handleKeyPress}
                placeholder="Type your message..."
                bg={inputBg}
                size="lg"
                disabled={sendMessageMutation.isPending}
              />
              <Button
                colorScheme="blue"
                size="lg"
                onClick={handleSendMessage}
                isLoading={sendMessageMutation.isPending}
                disabled={!inputMessage.trim()}
              >
                Send
              </Button>
            </HStack>
          </Box>
        </VStack>
      </HStack>
    </Container>
  );
};

interface MessageBubbleProps {
  message: Message;
  isUser: boolean;
  userName?: string;
}

const MessageBubble: React.FC<MessageBubbleProps> = ({ message, isUser, userName }) => {
  return (
    <HStack align="start" justify={isUser ? 'flex-end' : 'flex-start'}>
      {!isUser && <Avatar size="sm" name="AI" />}
      <VStack align={isUser ? 'flex-end' : 'flex-start'} spacing={2} maxW="80%">
        <Box
          bg={isUser ? 'blue.500' : 'gray.100'}
          color={isUser ? 'white' : 'black'}
          p={3}
          borderRadius="lg"
        >
          <Text whiteSpace="pre-wrap">{message.content}</Text>
        </Box>
        {message.sources && message.sources.length > 0 && (
          <Accordion allowToggle w="full">
            <AccordionItem border="none">
              <AccordionButton px={0}>
                <Box flex="1" textAlign="left">
                  <Badge colorScheme="blue">
                    {message.sources.length} Sources
                  </Badge>
                </Box>
                <AccordionIcon />
              </AccordionButton>
              <AccordionPanel px={0}>
                <VStack align="stretch" spacing={2}>
                  {message.sources.map((source: Source, index: number) => (
                    <Box key={index} p={2} bg="gray.50" borderRadius="md" fontSize="sm">
                      <Text fontWeight="bold">{source.document_title}</Text>
                      <Text noOfLines={3} color="gray.600">
                        {source.chunk_text}
                      </Text>
                      <Badge mt={1} colorScheme="green">
                        Score: {(source.score * 100).toFixed(1)}%
                      </Badge>
                    </Box>
                  ))}
                </VStack>
              </AccordionPanel>
            </AccordionItem>
          </Accordion>
        )}
      </VStack>
      {isUser && <Avatar size="sm" name={userName} />}
    </HStack>
  );
};

export default Chat;

