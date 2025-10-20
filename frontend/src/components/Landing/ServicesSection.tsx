import { Box, Container, Heading, Text, SimpleGrid, VStack, Icon, Flex } from "@chakra-ui/react"
import { useInView } from "react-intersection-observer"
import { FaBrain, FaHeart, FaUsers, FaChild, FaUserMd, FaHandHoldingHeart } from "react-icons/fa"

const services = [
  {
    icon: FaBrain,
    title: "Ansiedad y Estrés",
    description: "Tratamiento especializado para manejar la ansiedad, ataques de pánico y estrés crónico.",
  },
  {
    icon: FaHeart,
    title: "Depresión",
    description: "Apoyo profesional para superar la depresión y recuperar tu bienestar emocional.",
  },
  {
    icon: FaUsers,
    title: "Terapia de Pareja",
    description: "Fortalece tu relación y mejora la comunicación con tu pareja.",
  },
  {
    icon: FaChild,
    title: "Terapia Infantil",
    description: "Atención especializada para niños y adolescentes con un enfoque lúdico y empático.",
  },
  {
    icon: FaUserMd,
    title: "Trastornos de Conducta",
    description: "Intervención profesional para trastornos alimentarios, TOC y otros trastornos conductuales.",
  },
  {
    icon: FaHandHoldingHeart,
    title: "Desarrollo Personal",
    description: "Acompañamiento en tu proceso de crecimiento personal y autoconocimiento.",
  },
]

export default function ServicesSection() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.05 })

  return (
    <Box
      id="disorders"
      py={{ base: 16, md: 24 }}
      bg="gray.50"
      position="relative"
      ref={ref}
    >
      <Container maxW="1280px">
        <VStack gap={12}>
          <VStack
            gap={4}
            textAlign="center"
            opacity={inView ? 1 : 0}
            transform={inView ? "translateY(0)" : "translateY(30px)"}
            transition="all 0.6s"
          >
            <Heading
              as="h2"
              fontSize={{ base: "3xl", md: "4xl", lg: "5xl" }}
              fontWeight="700"
              color="gray.800"
            >
              Áreas de Especialización
            </Heading>
            <Text fontSize={{ base: "lg", md: "xl" }} color="gray.600" maxW="800px">
              Ofrecemos atención profesional en diversas áreas de la salud mental
            </Text>
          </VStack>

          <SimpleGrid columns={{ base: 1, md: 2, lg: 3 }} gap={8} w="full">
            {services.map((service, index) => (
              <Flex
                key={index}
                direction="column"
                bg="white"
                p={8}
                borderRadius="2xl"
                boxShadow="md"
                _hover={{ transform: "translateY(-8px)", boxShadow: "xl" }}
                transition="all 0.3s"
                opacity={inView ? 1 : 0}
                transform={inView ? "translateY(0)" : "translateY(30px)"}
                transitionDelay={`${index * 0.1}s`}
              >
                <Flex
                  w="64px"
                  h="64px"
                  align="center"
                  justify="center"
                  bg="rgba(255, 167, 38, 0.1)"
                  borderRadius="xl"
                  mb={4}
                >
                  <Icon as={service.icon} fontSize="2xl" color="#FFA726" />
                </Flex>
                <Heading as="h3" fontSize="xl" fontWeight="600" color="gray.800" mb={3}>
                  {service.title}
                </Heading>
                <Text color="gray.600" lineHeight="1.7">
                  {service.description}
                </Text>
              </Flex>
            ))}
          </SimpleGrid>
        </VStack>
      </Container>
    </Box>
  )
}
