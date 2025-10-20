import { Box, Container, Heading, Text, VStack, Image, IconButton, Flex } from "@chakra-ui/react"
import { useInView } from "react-intersection-observer"
import useEmblaCarousel from "embla-carousel-react"
import { useCallback } from "react"
import { FaChevronLeft, FaChevronRight } from "react-icons/fa"
import Autoplay from "embla-carousel-autoplay"

const carouselImages = [
  { src: "/assets/landing/carrusel/1.webp", alt: "Espacio de la clínica Conectemos Chile 1" },
  { src: "/assets/landing/carrusel/2.webp", alt: "Espacio de la clínica Conectemos Chile 2" },
  { src: "/assets/landing/carrusel/3.webp", alt: "Espacio de la clínica Conectemos Chile 3" },
  { src: "/assets/landing/carrusel/4.webp", alt: "Espacio de la clínica Conectemos Chile 4" },
]

export default function SpaceCarousel() {
  const { ref, inView } = useInView({ triggerOnce: true, threshold: 0.1 })
  const [emblaRef, emblaApi] = useEmblaCarousel({ loop: true }, [
    Autoplay({ delay: 5000, stopOnInteraction: false }),
  ])

  const scrollPrev = useCallback(() => {
    if (emblaApi) emblaApi.scrollPrev()
  }, [emblaApi])

  const scrollNext = useCallback(() => {
    if (emblaApi) emblaApi.scrollNext()
  }, [emblaApi])

  return (
    <Box
      id="space"
      py={{ base: 16, md: 24 }}
      bg="white"
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
              Nuestro Espacio
            </Heading>
            <Text fontSize={{ base: "lg", md: "xl" }} color="gray.600" maxW="800px">
              Un ambiente acogedor y profesional diseñado para tu comodidad
            </Text>
          </VStack>

          <Box
            position="relative"
            w="full"
            maxW="900px"
            mx="auto"
            opacity={inView ? 1 : 0}
            transform={inView ? "scale(1)" : "scale(0.95)"}
            transition="all 0.8s 0.2s"
          >
            <Box ref={emblaRef} overflow="hidden" borderRadius="2xl">
              <Flex>
                {carouselImages.map((image, index) => (
                  <Box
                    key={index}
                    flex="0 0 100%"
                    minW={0}
                  >
                    <Image
                      src={image.src}
                      alt={image.alt}
                      w="full"
                      h={{ base: "300px", md: "500px" }}
                      objectFit="cover"
                    />
                  </Box>
                ))}
              </Flex>
            </Box>

            {/* Navigation buttons */}
            <IconButton
              aria-label="Anterior"
              icon={<FaChevronLeft />}
              position="absolute"
              left={4}
              top="50%"
              transform="translateY(-50%)"
              onClick={scrollPrev}
              bg="whiteAlpha.900"
              _hover={{ bg: "white" }}
              boxShadow="lg"
              borderRadius="full"
              zIndex={2}
            />
            <IconButton
              aria-label="Siguiente"
              icon={<FaChevronRight />}
              position="absolute"
              right={4}
              top="50%"
              transform="translateY(-50%)"
              onClick={scrollNext}
              bg="whiteAlpha.900"
              _hover={{ bg: "white" }}
              boxShadow="lg"
              borderRadius="full"
              zIndex={2}
            />
          </Box>
        </VStack>
      </Container>
    </Box>
  )
}
