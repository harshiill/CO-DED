'use client'
import {
    Button,
    Paper,
    PaperProps,
    Stack,
    Text,
    TextInput,
    Container,
    Center,
    Title,
    Group,
    ActionIcon
} from '@mantine/core';
import { useForm } from '@mantine/form';
import { IconWorld, IconPlus, IconTrash } from '@tabler/icons-react';
import { useState } from 'react';

export function URLInputForm(props: PaperProps) {
    const [urls, setUrls] = useState([{ id: Date.now(), value: '' }]);
    const [loading, setLoading] = useState(false);

    const form = useForm({
        initialValues: {
            urls: urls.map(urlObj => urlObj.value),
        },
        validate: {
            urls: (values) =>
                values.some(val => !/^(https?:\/\/)?([\w.-]+\.[a-z]{2,})(\/.*)?$/.test(val))
                ? 'Invalid URL'
                : null,            
        },
    });

    // Add new URL field
    const addUrlField = () => {
        setUrls([...urls, { id: Date.now(), value: '' }]);
    };

    // Remove a URL field
    const removeUrlField = (id: number) => {
        setUrls(urls.filter(url => url.id !== id));
    };

    // Update field value
    const updateUrlValue = (id: number, value: string) => {
        setUrls(urls.map(url => (url.id === id ? { ...url, value } : url)));
    };

    // Handle form submission
    const handleSubmit = async () => {
        try {
            const response = await fetch('http://localhost:8000/api/submit', {  // <-- Change this URL if needed
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ urls }),
            });
    
            const data = await response.json();
            console.log('Server response:', data);
    
            if (response.ok) {
                alert('URLs submitted successfully!');
            } else {
                alert(`Failed: ${data.message || 'Unknown error'}`);
            }
        } catch (error) {
            console.error('Submission error:', error);
            alert('Network error. Check console.');
        }
    };
    

    return (
        <Container size={420} my={40} className="url-container">
            <Center>
                <IconWorld size={48} stroke={1.5} className="icon-world" />
            </Center>
            <Title ta="center" order={2} fw={700} className="title">
                URL Submission
            </Title>
            <Text color="dimmed" size="sm" ta="center" mt={5} className="subtitle">
                Enter valid website URLs below
            </Text>

            <Paper radius="lg" p="xl" withBorder shadow="md" mt={20} {...props} className="url-paper">
                <form onSubmit={(e) => {
                    e.preventDefault();
                    handleSubmit();
                }}>
                    <Stack gap="md" align="center" justify='center' display='flex'>
                        {urls.map((urlObj, index) => (
                            <Group key={urlObj.id} align="center" justify='center' display='flex' style={{ width: '100%' }}>
                                <h4>Website URL {index + 1}</h4>
                                <TextInput
                                    required
                                    placeholder="https://example.com"
                                    value={urlObj.value}
                                    onChange={(event) => updateUrlValue(urlObj.id, event.currentTarget.value)}
                                    error={form.errors.urls && 'Invalid URL'}
                                    radius="md"
                                    size="md"
                                    className="url-input"
                                    style={{ flexGrow: 1 }} // Ensures input stretches
                                />
                                {urls.length > 1 && (
                                    <ActionIcon 
                                        onClick={() => removeUrlField(urlObj.id)} 
                                        color="red" 
                                        variant="light"
                                        size="md"
                                        style={{ 
                                            display: "flex", 
                                            alignItems: "center", 
                                            justifyContent: "center", 
                                            height: '40px' // Matches input height
                                        }}
                                    >
                                        <IconTrash size={20} />
                                    </ActionIcon>
                                )}
                            </Group>
                        ))}
                    </Stack>

                    <Group justify="center" mt="md">
                        <Button onClick={addUrlField} variant="light" radius="xl" size="md" className="add-url-button">
                            <IconPlus size={16} /> Add URL
                        </Button>
                    </Group>

                    <Group justify="center" mt="xl">
                        <Button type="submit" radius="xl" size="md" color="blue" className="submit-button" loading={loading}>
                            {loading ? 'Submitting...' : 'Submit URLs'}
                        </Button>
                    </Group>
                </form>
            </Paper>
        </Container>
    );
}
