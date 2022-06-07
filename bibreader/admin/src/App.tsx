import { yupResolver } from "@hookform/resolvers/yup"
import {
    Button,
    Dialog,
    DialogActions,
    DialogContent,
    DialogTitle,
} from "@mui/material"
import { useSnackbar } from "notistack"
import React, { useState } from "react"
import { FormProvider, useForm } from "react-hook-form"
import styled from "styled-components"
import * as yup from "yup"
import FText from "./FText"

const Date = styled.div`
    display: flex;
    gap: 10px;
`

const SDialogContent = styled(DialogContent)`
    display: flex;
    flex-direction: column;
    gap: 1rem;
`

const dataSchema = yup.object().shape({
    quantity: yup.number().min(0).max(10000).default(0),
    e_year: yup.number().min(2021).max(2100).default(2022),
    e_month: yup.number().min(1).max(12).default(1),
    e_day: yup.number().min(1).max(31).default(1),
    type: yup.string().min(10).max(10).default(""),
})

function App() {
    const { enqueueSnackbar } = useSnackbar()
    const [bibID, setBibID] = useState<string>("")

    const form = useForm({
        resolver: yupResolver(dataSchema),
        defaultValues: dataSchema.getDefault(),
    })

    const read = () => {
        fetch("/api").then((res) => {
            if (res.status === 200) {
                res.json().then((j) => {
                    setBibID(j.id)
                    form.reset(j.data)
                    enqueueSnackbar("Bib lu avec succès", {
                        variant: "success",
                    })
                })
            } else {
                res.text().then((err) => {
                    enqueueSnackbar(err, { variant: "error" })
                })
            }
        })
    }

    const onSubmit = (values: any) => {
        fetch("/api", {
            method: "POST",
            body: JSON.stringify({
                id: bibID,
                data: values,
            }),
        }).then((res) => {
            if (res.status === 200) {
                enqueueSnackbar("Bib écrit avec succès", { variant: "success" })
            } else {
                res.text().then((err) => {
                    enqueueSnackbar(err, { variant: "error" })
                })
            }
        })
    }

    return (
        <FormProvider {...form}>
            <Dialog open={true}>
                <DialogTitle>Bib : {bibID === "" ? "..." : bibID}</DialogTitle>
                <SDialogContent dividers>
                    <FText label="Quantité" name="quantity" />
                    <Date>
                        <FText label="Année" name="e_year" />
                        <FText label="Mois" name="e_month" />
                        <FText label="Jour" name="e_day" />
                    </Date>
                    <FText label="Type" name="type" />
                </SDialogContent>
                <DialogActions>
                    <Button variant="contained" onClick={read}>
                        Lire
                    </Button>
                    <Button
                        variant="contained"
                        onClick={form.handleSubmit(onSubmit)}
                    >
                        Ecrire
                    </Button>
                </DialogActions>
            </Dialog>
        </FormProvider>
    )
}

export default App
