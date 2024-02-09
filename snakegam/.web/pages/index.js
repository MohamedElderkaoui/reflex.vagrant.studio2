/** @jsxImportSource @emotion/react */


import { Fragment, useCallback, useContext, useEffect } from "react"
import { Fragment_fd0e7cb8f9fb4669a6805377d925fba0 } from "/utils/stateful_components"
import { Box, Button, Heading, HStack, SimpleGrid, Switch, VStack } from "@chakra-ui/react"
import { EventLoopContext, StateContexts } from "/utils/context"
import { Event, isTrue } from "/utils/state"
import "@radix-ui/themes/styles.css"
import "focus-visible/dist/focus-visible"
import { Theme as RadixThemesTheme } from "@radix-ui/themes"
import NextHead from "next/head"



export function Button_c1338eddb128286e819b0a8e750e7fd7 () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_dc8af2191d08dc907a9a3ebc03a9e5d6 = useCallback((_e) => addEvents([Event("state.state.arrow_down", {})], (_e), {}), [addEvents, Event])

  return (
    <Button colorScheme={`red`} onClick={on_click_dc8af2191d08dc907a9a3ebc03a9e5d6} sx={{"borderRadius": "1em", "fontSize": "2em"}}>
  {`￬`}
</Button>
  )
}

export function Simplegrid_337a16b6083803a88873f4e5448336ab () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <SimpleGrid columns={[19]}>
  {state__state.cells.map((color, idx) => (
  <Box key={idx} sx={{"bg": color, "width": "1em", "height": "1em", "border": "1px solid white"}}/>
))}
</SimpleGrid>
  )
}

export function Switch_8121c8ebdffa1aedc7d8b82ff80783aa () {
  const [addEvents, connectError] = useContext(EventLoopContext);
  const state__state = useContext(StateContexts.state__state)

  const on_change_6f4004c6fbf89baebd209745225b5e6f = useCallback((_e0) => addEvents([Event("state.state.flip_switch", {start:_e0.target.checked})], (_e0), {}), [addEvents, Event])

  return (
    <Switch isChecked={state__state.running} onChange={on_change_6f4004c6fbf89baebd209745225b5e6f} value={true}/>
  )
}

export function Button_6ff1dbf4fa877fdefa9f4c9323db7a0f () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_3006791a0bff96622d160fe227403b7b = useCallback((_e) => addEvents([Event("state.state.play", {})], (_e), {}), [addEvents, Event])

  return (
    <Button colorScheme={`green`} onClick={on_click_3006791a0bff96622d160fe227403b7b} sx={{"borderRadius": "1em"}}>
  {`RUN`}
</Button>
  )
}

export function Fragment_22553b2d485e03c3c7040cf7a54e955a () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <Fragment>
  {isTrue(state__state.died) ? (
  <Fragment>
  <Heading>
  {`Game Over 🐍`}
</Heading>
</Fragment>
) : (
  <Fragment/>
)}
</Fragment>
  )
}

export function Button_6f70c0775d94e09d26cd091a459cd38a () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_098f821a8f37366cddc410c655327c40 = useCallback((_e) => addEvents([Event("state.state.arrow_up", {})], (_e), {}), [addEvents, Event])

  return (
    <Button colorScheme={`red`} onClick={on_click_098f821a8f37366cddc410c655327c40} sx={{"borderRadius": "1em", "fontSize": "2em"}}>
  {`￪`}
</Button>
  )
}

export function Heading_eb7c719f13eed5ebe4d29ba7354a214d () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <Heading sx={{"fontSize": "2em"}}>
  {state__state.magic}
</Heading>
  )
}

export function Button_b6d19c7a273d2e4029a13dd4ee487a1c () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_9e6346a84c1f11d809a690aeb07dcaaa = useCallback((_e) => addEvents([Event("state.state.arrow_right", {})], (_e), {}), [addEvents, Event])

  return (
    <Button colorScheme={`red`} onClick={on_click_9e6346a84c1f11d809a690aeb07dcaaa} sx={{"borderRadius": "1em", "fontSize": "2em"}}>
  {`￫`}
</Button>
  )
}

export function Heading_15c5658a00fa1177e945be716bacc987 () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <Heading sx={{"fontSize": "2em"}}>
  {state__state.score}
</Heading>
  )
}

export function Button_933923be7ad15be929f2461fc1735e27 () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_8748aa04708177d88e38a19c95d0e447 = useCallback((_e) => addEvents([Event("state.state.arrow_left", {})], (_e), {}), [addEvents, Event])

  return (
    <Button colorScheme={`red`} onClick={on_click_8748aa04708177d88e38a19c95d0e447} sx={{"borderRadius": "1em", "fontSize": "2em"}}>
  {`￩`}
</Button>
  )
}

export function Button_6bd10e2131a8d5501a1db8d4eccba867 () {
  const [addEvents, connectError] = useContext(EventLoopContext);

  const on_click_3319dd1363fd64c159a41fe762c883e7 = useCallback((_e) => addEvents([Event("state.state.pause", {})], (_e), {}), [addEvents, Event])

  return (
    <Button colorScheme={`blue`} onClick={on_click_3319dd1363fd64c159a41fe762c883e7} sx={{"borderRadius": "1em"}}>
  {`PAUSE`}
</Button>
  )
}

export function Heading_1422380c8efbc1e326e90f1184d66e72 () {
  const state__state = useContext(StateContexts.state__state)


  return (
    <Heading sx={{"fontSize": "2em"}}>
  {state__state.rate}
</Heading>
  )
}

export default function Component() {
  
useEffect(() => {
    const handle_key = (_e0) => {
        if (["ArrowUp", "ArrowLeft", "ArrowRight", "ArrowDown", ",", "."].includes(_e0.key))
            addEvents([Event("state.state.handle_key", {key:_e0.key})])
    }
    document.addEventListener("keydown", handle_key, false);
    return () => {
        document.removeEventListener("keydown", handle_key, false);
    }
})

  const [addEvents, connectError] = useContext(EventLoopContext);

  return (
    <Fragment>
  <Fragment_fd0e7cb8f9fb4669a6805377d925fba0/>
  <VStack sx={{"paddingTop": "3%"}}>
  <HStack>
  <Button_6bd10e2131a8d5501a1db8d4eccba867/>
  <Button_6ff1dbf4fa877fdefa9f4c9323db7a0f/>
  <Switch_8121c8ebdffa1aedc7d8b82ff80783aa/>
</HStack>
  <HStack>
  <VStack sx={{"bgColor": "yellow", "borderWidth": "1px", "paddingLeft": "1em", "paddingRight": "1em"}}>
  <Heading sx={{"fontSize": "1em"}}>
  {`RATE`}
</Heading>
  <Heading_1422380c8efbc1e326e90f1184d66e72/>
</VStack>
  <VStack sx={{"bgColor": "yellow", "borderWidth": "1px", "paddingLeft": "1em", "paddingRight": "1em"}}>
  <Heading sx={{"fontSize": "1em"}}>
  {`SCORE`}
</Heading>
  <Heading_15c5658a00fa1177e945be716bacc987/>
</VStack>
  <VStack sx={{"bgColor": "yellow", "borderWidth": "1px", "paddingLeft": "1em", "paddingRight": "1em"}}>
  <Heading sx={{"fontSize": "1em"}}>
  {`MAGIC`}
</Heading>
  <Heading_eb7c719f13eed5ebe4d29ba7354a214d/>
</VStack>
</HStack>
  <Simplegrid_337a16b6083803a88873f4e5448336ab/>
  <Fragment_22553b2d485e03c3c7040cf7a54e955a/>
  <HStack>
  
  <VStack>
  <Button colorScheme={`none`} sx={{"borderRadius": "1em", "fontSize": "2em"}}>
  {`￮`}
</Button>
  <Button_933923be7ad15be929f2461fc1735e27/>
</VStack>
  <VStack>
  <Button_6f70c0775d94e09d26cd091a459cd38a/>
  <Button_c1338eddb128286e819b0a8e750e7fd7/>
</VStack>
  <VStack>
  <Button colorScheme={`none`} sx={{"borderRadius": "1em", "fontSize": "2em"}}>
  {`￮`}
</Button>
  <Button_b6d19c7a273d2e4029a13dd4ee487a1c/>
</VStack>
</HStack>
</VStack>
  <NextHead>
  <title>
  {`snake game`}
</title>
  <meta content={`A Reflex app.`} name={`description`}/>
  <meta content={`favicon.ico`} property={`og:image`}/>
</NextHead>
</Fragment>
  )
}
