import React, { useState, useRef } from 'react';
import {
  Box,
  Button,
  Container,
  Heading,
  Table,
  Thead,
  Tbody,
  Tr,
  Th,
  Td,
  Badge,
  IconButton,
  useDisclosure,
  Modal,
  ModalOverlay,
  ModalContent,
  ModalHeader,
  ModalBody,
  ModalCloseButton,
  ModalFooter,
  FormControl,
  FormLabel,
  Input,
  VStack,
  HStack,
  Text,
  useColorModeValue,
  Spinner,
  Center,
  Textarea,
  useToast,
} from '@chakra-ui/react';
import { AddIcon, DeleteIcon, ViewIcon } from '@chakra-ui/icons';
import { useDocuments, useUploadDocument, useDeleteDocument } from '@/hooks/useDocuments';
import { Document } from '@/types';

const Documents: React.FC = () => {
  const { data: documents, isLoading } = useDocuments();
  const uploadMutation = useUploadDocument();
  const deleteMutation = useDeleteDocument();
  const { isOpen, onOpen, onClose } = useDisclosure();
  const fileInputRef = useRef<HTMLInputElement>(null);
  const toast = useToast();

  const [selectedFile, setSelectedFile] = useState<File | null>(null);
  const [title, setTitle] = useState('');
  const [description, setDescription] = useState('');

  const cardBg = useColorModeValue('white', 'gray.700');

  const handleFileSelect = (e: React.ChangeEvent<HTMLInputElement>) => {
    const file = e.target.files?.[0];
    if (file) {
      setSelectedFile(file);
      setTitle(file.name);
    }
  };

  const handleUpload = async () => {
    if (!selectedFile) {
      toast({
        title: 'No file selected',
        status: 'warning',
        duration: 3000,
      });
      return;
    }

    try {
      await uploadMutation.mutateAsync({
        file: selectedFile,
        title,
        description,
      });
      setSelectedFile(null);
      setTitle('');
      setDescription('');
      onClose();
    } catch (error) {
      // Error handled by mutation
    }
  };

  const handleDelete = async (id: string) => {
    if (window.confirm('Are you sure you want to delete this document?')) {
      await deleteMutation.mutateAsync(id);
    }
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'completed':
        return 'green';
      case 'processing':
        return 'blue';
      case 'uploading':
        return 'yellow';
      case 'failed':
        return 'red';
      default:
        return 'gray';
    }
  };

  const formatFileSize = (bytes: number) => {
    if (bytes < 1024) return bytes + ' B';
    if (bytes < 1024 * 1024) return (bytes / 1024).toFixed(2) + ' KB';
    return (bytes / (1024 * 1024)).toFixed(2) + ' MB';
  };

  if (isLoading) {
    return (
      <Center h="50vh">
        <Spinner size="xl" />
      </Center>
    );
  }

  return (
    <Container maxW="container.xl" py={8}>
      <VStack align="stretch" spacing={6}>
        <HStack justify="space-between">
          <Heading size="lg">Documents</Heading>
          <Button leftIcon={<AddIcon />} colorScheme="blue" onClick={onOpen}>
            Upload Document
          </Button>
        </HStack>

        <Box
          bg={cardBg}
          borderRadius="lg"
          shadow="md"
          borderWidth="1px"
          overflow="hidden"
        >
          {documents && documents.length > 0 ? (
            <Table variant="simple">
              <Thead>
                <Tr>
                  <Th>Title</Th>
                  <Th>File Type</Th>
                  <Th>Size</Th>
                  <Th>Status</Th>
                  <Th>Uploaded</Th>
                  <Th>Actions</Th>
                </Tr>
              </Thead>
              <Tbody>
                {documents.map((doc: Document) => (
                  <Tr key={doc.id}>
                    <Td>
                      <VStack align="start" spacing={0}>
                        <Text fontWeight="medium">{doc.title}</Text>
                        {doc.description && (
                          <Text fontSize="sm" color="gray.600" noOfLines={1}>
                            {doc.description}
                          </Text>
                        )}
                      </VStack>
                    </Td>
                    <Td>
                      <Badge>{doc.file_type}</Badge>
                    </Td>
                    <Td>{formatFileSize(doc.file_size)}</Td>
                    <Td>
                      <Badge colorScheme={getStatusColor(doc.status)}>
                        {doc.status}
                      </Badge>
                    </Td>
                    <Td>
                      {new Date(doc.created_at).toLocaleDateString()}
                    </Td>
                    <Td>
                      <HStack spacing={2}>
                        <IconButton
                          aria-label="Delete"
                          icon={<DeleteIcon />}
                          size="sm"
                          colorScheme="red"
                          variant="ghost"
                          onClick={() => handleDelete(doc.id)}
                          isLoading={deleteMutation.isPending}
                        />
                      </HStack>
                    </Td>
                  </Tr>
                ))}
              </Tbody>
            </Table>
          ) : (
            <Box p={8} textAlign="center">
              <Text color="gray.600">
                No documents uploaded yet. Click "Upload Document" to get started.
              </Text>
            </Box>
          )}
        </Box>
      </VStack>

      {/* Upload Modal */}
      <Modal isOpen={isOpen} onClose={onClose} size="lg">
        <ModalOverlay />
        <ModalContent>
          <ModalHeader>Upload Document</ModalHeader>
          <ModalCloseButton />
          <ModalBody>
            <VStack spacing={4}>
              <FormControl>
                <FormLabel>Select File</FormLabel>
                <Input
                  type="file"
                  ref={fileInputRef}
                  onChange={handleFileSelect}
                  accept=".pdf,.docx,.txt,.csv,.md"
                />
                {selectedFile && (
                  <Text mt={2} fontSize="sm" color="gray.600">
                    Selected: {selectedFile.name} ({formatFileSize(selectedFile.size)})
                  </Text>
                )}
              </FormControl>
              <FormControl>
                <FormLabel>Title</FormLabel>
                <Input
                  value={title}
                  onChange={(e) => setTitle(e.target.value)}
                  placeholder="Document title"
                />
              </FormControl>
              <FormControl>
                <FormLabel>Description (Optional)</FormLabel>
                <Textarea
                  value={description}
                  onChange={(e) => setDescription(e.target.value)}
                  placeholder="Document description"
                  rows={3}
                />
              </FormControl>
            </VStack>
          </ModalBody>
          <ModalFooter>
            <Button variant="ghost" mr={3} onClick={onClose}>
              Cancel
            </Button>
            <Button
              colorScheme="blue"
              onClick={handleUpload}
              isLoading={uploadMutation.isPending}
              isDisabled={!selectedFile}
            >
              Upload
            </Button>
          </ModalFooter>
        </ModalContent>
      </Modal>
    </Container>
  );
};

export default Documents;

