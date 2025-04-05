"use client";

import { Button, Card, Container, Stack, Text, Title, Anchor } from '@mantine/core';
import { Github } from "lucide-react";

export default function Home() {
  const githubPrUrl = "https://github.com/yourusername/yourrepository/compare";

  return (
    <main style={{ minHeight: "100vh", display: "flex", alignItems: "center", justifyContent: "center" }}>
      <Container size="xs">
        <Card shadow="xl" radius="lg" p="xl" withBorder>
          <Stack align="center" gap="md">
            <Title order={2} ta="center">
              GitHub PR Creator
            </Title>

            <Text c="dimmed" ta="center">
              Click the button below to create a new Pull Request
            </Text>

            <Anchor href={githubPrUrl} target="_blank" rel="noopener noreferrer" underline="never">
              <Button
                leftSection={<Github size={20} />}
                size="md"
                variant="filled"
                color="dark"
                radius="md"
              >
                Need a PR
              </Button>
            </Anchor>
          </Stack>
        </Card>
      </Container>
    </main>
  );
}
